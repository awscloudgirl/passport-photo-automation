# Cloudtopia Passport Office Automation Project

![Cloudtopia Passport Office Automation](CloudtopiaPassportPhotoAutomation.png)

## Introducing the Cloudtopia Passport Office Automation Project: Enhancing Passport Photo Validation with Robust Architecture

### Project Overview

Traditionally, citizens applying for passports faced a manual evaluation process for submitted photographs, with strict adherence to guidelines. My project not only automates this process but also fulfills crucial architectural requirements to ensure efficiency, scalability, and reliability.

### Introduction

As an employee of the Cloudtopia Passport Office—a Federal agency responsible for issuing passports to the fine citizens of Cloudtopia—I am tasked with simplifying the Passport Photo Validation process using automation.

Currently, citizens of Cloudtopia who wish to apply for a passport must submit a photograph of themselves. For the photograph to be accepted, it must adhere to strict requirements: the applicant's face must be clearly visible, they must not be wearing sunglasses, their eyes must be open, and they must not be smiling.

For example:
- An image with the applicant’s eyes closed would fail the evaluation process.
- An image with the applicant smiling would also fail.
- An image adhering to all guidelines would be accepted.

In the current Photo Validation process, applicants submit their photographs through a web endpoint. An agency employee then evaluates the image to ensure it adheres to guidelines and either accepts or rejects it, providing a reason for rejection if necessary.

The Cloudtopia Passport Office has three main requirements for this project:

1. **Automation**: Remove the need for a human to evaluate submitted photographs.
2. **Notifications**: Broadcast notifications to other services within Cloudtopia whenever a photo evaluation is completed.
3. **API Access**: Provide a means to access the result of the photo evaluation through an API, detailing any reasons for rejection.

By automating the photo validation process, I aim to streamline passport issuance, reduce human error, and improve overall efficiency.

---

### Key Components:

1. **Image Storage:**
   Our system incorporates a robust Image Storage component capable of handling large and small user-submitted photos. With a focus on fast uploads and durability, this component ensures optimal latency and throughput for seamless user experience.

2. **Compute:**
   The Compute component reacts to file uploads, offering two options: polling for new images or leveraging an event-driven architecture. Prioritizing reliability and high performance, this component guarantees swift processing of uploaded images.

3. **Facial Recognition:**
   At the core of our application is Facial Recognition, detecting facial features with confidence. Designed for scalability and low latency, this component utilizes advanced facial recognition libraries to provide accurate analysis of submitted images.

4. **Database:**
   Our architecture incorporates a performant and scalable key-value lookup store for storing approval/rejection details and references to images. This Database component ensures efficient data management, supporting the dynamic needs of our system.

5. **Notifications:**
   Leveraging Notifications, our system publishes messages to client services upon image evaluation. This decoupling of microservices enhances system flexibility and avoids dependence on a centralized "uber database," contributing to a more resilient and adaptable architecture.

6. **API:**
   The API component exposes additional information about evaluation results, providing a seamless interface for retrieving details. This ensures transparency and accessibility, allowing for easy integration with external systems.

These six themes form the foundation of our architecture, ensuring a comprehensive and well-rounded solution. 

## Core Technology Choices: Powering the Cloudtopia Passport Office Automation Project**

In the pursuit of an efficient and scalable solution, we've carefully selected core technologies that seamlessly integrate to deliver a robust Passport Photo Validation system.

### Part 1: Image Processing

*Technology Stack: S3, Lambda, Amazon Rekognition, DynamoDB*

We have chosen Amazon S3 as our go-to solution for image file storage, offering the scalability needed to accommodate varying sizes of user-submitted photos. Upon image upload, our system is orchestrated to trigger a Lambda function. The Lambda function, intricately coded, harnesses the capabilities of Amazon Rekognition, providing advanced facial analysis. The evaluated results are then securely stored in DynamoDB, ensuring a performant and scalable key-value lookup store for approval/rejection details.

### Part 2: Notifications

*Technology Stack: Lambda, Lambda Destinations, SNS (Simple Notification Service)*

To seamlessly handle notifications, we employ Lambda Destinations—a powerful feature within Lambda. Leveraging this capability, the results of a Lambda function invocation are effortlessly directed to another AWS service. In our case, Lambda Destinations facilitates the smooth transmission of results to our SNS (Simple Notification Service) topic. This ensures timely and efficient delivery of messages to client services, promoting a decoupled and resilient microservices architecture.

### Part 3: Data Retrieval

*Technology Stack: API Gateway, Lambda, DynamoDB*

For data retrieval, we implement an API gateway endpoint seamlessly integrated with Lambda functions. This gateway is purposefully designed to query our DynamoDB database, allowing for swift and accurate retrieval of information related to image evaluations. This cohesive integration ensures a user-friendly API interface for external systems, promoting transparency and accessibility.

By combining these core technologies, our architecture not only fulfills the unique requirements of each project phase but also ensures a cohesive and streamlined workflow. As you delve into our GitHub repository, witness the synergy of S3, Lambda, Amazon Rekognition, DynamoDB, Lambda Destinations, SNS, API Gateway, and more, contributing to the success of the Cloudtopia Passport Office Automation Project.
