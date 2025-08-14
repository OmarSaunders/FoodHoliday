Project Name: TFL - Food Holiday Application
Date Created: April 1, 2025
Created By: Omar Saunders
Status: Completed

1. 🎯 Business Use Case


The core request from our client was for a comprehensive and dynamic source of information pertaining to various culinary and food traditions. She specifically emphasized a need for insights beyond her existing knowledge base, indicating a desire for novel and diverse perspectives on global food culture.
To address this, the client articulated a clear preference for a system that could proactively deliver relevant information. Her stated methods for receiving these updates included either direct email notifications or alerts prompting her to visit a dedicated online platform. The primary objective of these notifications is to provide her with the necessary and timely information she requires to stay abreast of various food-related holidays, celebrations, and cultural practices. This suggests a need for a solution that is both informative and convenient, minimizing the effort required on her part to access the desired content.

Target Audience / Stakeholders
Owner of TFL by Jazzmine
Business Value
This application will enable the creation of content centered around the food holiday corresponding to the current date.

2. ☁️ Cloud Architecture Overview
Cloud Provider(s)
Google Cloud
Architecture Type
Serverless 


3. ⚙️ Services & Tools
Layer	Services/Tools	Description
Programming Language	Python	Python is a high-level, interpreted, versatile, and readable language
Serverless	Google Cloud Functions	Run code snippets on demand, no servers to manage
Notification	Pub/Sub	Publishers send messages to topics, subscribers receive messages.
Event Driver	Cloud Scheduler	Fully managed enterprise-grade cron job scheduler.
Storage	Google Cloud Storage	Storing logs within Storage Bucket
Infrastructure	 Terraform	Defining resources as code
Secrets	GCP Secrets Manager	Credential management
Identity	IAM	Access and identity control

4. 🛠️ Dev & Deployment Workflow
Code Repository
 https://github.com/OmarSaunders/FoodHoliday
Branching Strategy
Main Branch 
CI/CD Pipeline
    • At this moment in time it isn't needed. 
    • Will be required once I expound and advance the python applicatio


5. 🔐 Security
    • IAM roles & least privilege



6. 💲 Cost Optimization
    • This project will cost me nothing

    



8. 📈 Success Criteria & KPIs
    • Notification sent and received




