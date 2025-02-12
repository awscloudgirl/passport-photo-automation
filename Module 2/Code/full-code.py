import json
import boto3
import uuid
import datetime 

BUCKET_NAME = "cloudtopia-images" 
FACE_DETAILS_THRESHOLDS = {"Smile": {"desiredValue": False, "minConfidence": 90}, "Sunglasses": {"desiredValue": False, "minConfidence": 90}, "EyesOpen": {"desiredValue": True, "minConfidence": 90}, "MouthOpen": {"desiredValue": False, "minConfidence": 90}}

rekognition_client = boto3.client('rekognition')
dynamodb_client = boto3.resource('dynamodb')

validation_table = dynamodb_client.Table('ValidationRequests') 

def lambda_handler(event, context):
    
    #Step 1 - Extract File Name from PUT Event
    current_file_name = extract_file_name(event)
    
    #Step 2 - Call Rekognition DetectFaces API
    detect_faces_response = detect_faces(current_file_name)
    
    #Step 3 - Extract face details we care about and their value/confidence
    face_details = extract_face_details(detect_faces_response) #extract the attributes we care about

    #Step 4 - Evaluates values and thresholds to determine PASS/FAIL
    face_evaluation_result = evaluate_face(face_details)

    #Step 5 - Write Results to DynamoDB
    saved_result = write_result_to_dynamo(face_evaluation_result, current_file_name, face_details)

    #Step 6 - Pipe result using Lambda Destinations
    publish_object = {
        'FileName': current_file_name,
        'ValidationResult': face_evaluation_result['result'],
        'FailureReasons': json.dumps(face_evaluation_result['failure_reasons']),
        'FileLocation': BUCKET_NAME + "/" + current_file_name,
    }
    return {
        'statusCode': 200,
        'body': json.dumps(publish_object)
    }
    
def write_result_to_dynamo(evaluation_result, file_name, face_details):

    # Set the item attributes
    item_attributes = {
            'FileName': file_name,
            'ValidationResult': evaluation_result['result'],
            'FailureReasons': json.dumps(evaluation_result['failure_reasons']),
            'Timestamp': datetime.datetime.now().replace(microsecond=0).isoformat(),
            'FileLocation': BUCKET_NAME + "/" + file_name,
            'FaceDetails': json.dumps(face_details)
            
    }
    
    response = validation_table.put_item(
        Item=item_attributes)
    
    # Check the response to see if the item was added successfully
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Item added to table successfully!')
    else:
        print('Error adding item to table.')

def evaluate_face(parsed_face_scan):

    evaluation_result = {
        "result": "PASS", #we assume it is a pass unless we prove otherwise
        "failure_reasons": []
    }
    
    for key, value in FACE_DETAILS_THRESHOLDS.items():
        temp_result = True #assume we pass the test
        if parsed_face_scan[key]["Value"] != FACE_DETAILS_THRESHOLDS[key]["desiredValue"]:
            print(f"Expected != Actual. FaceAttribute: {key} has a value: {parsed_face_scan[key]['Value']}, but requires {FACE_DETAILS_THRESHOLDS[key]['desiredValue']}")
            temp_result = False
        if parsed_face_scan[key]["Confidence"] <= FACE_DETAILS_THRESHOLDS[key]["minConfidence"]:
            print(f"Confidence is lower than minimum threshold. FaceAttribute: {key} has a confidence value: {parsed_face_scan[key]['Confidence']}, but must be greater than {FACE_DETAILS_THRESHOLDS[key]['minConfidence']}")
            temp_result = False
        
        if temp_result is False:
            evaluation_result["result"] = "FAIL"
            evaluation_result["failure_reasons"].append(key)
    return evaluation_result

def extract_face_details(result):
    parsed_response = {} 
    
    face_details = result["FaceDetails"]
    face = face_details[0]
    
    #iterate over all fields we care about and extract the details
    for key, value in FACE_DETAILS_THRESHOLDS.items():
        parsed_response[key] = face[key]
        
    return parsed_response

def detect_faces(file_name):
    return rekognition_client.detect_faces(
    Image={
        'S3Object': {
            'Bucket': BUCKET_NAME,
            'Name': file_name
        }
    },
    Attributes=['ALL']
    )
    
def extract_file_name(event):
    return event["Records"][0]["s3"]["object"]["key"]