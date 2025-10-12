# Food Holiday Notification Automation

 Delivers the customer the designated food holiday for Today’s date

---

##  Purpose / Problem Statement
My client is a content creator within the baking industry and she wanted to be informed of information that could help her create content. By creating this python application, she will be informed of relevant information each and every day at 8:00 AM

---



## Tech & Tooling Stack
| Layer | Tool / Service | Why Chosen |
|-------|----------------|-----------|
| **Cloud Provider** | Cloud Functions was chosen due to its event-driven nature. Cloud Scheduler will invoke the Cloud Functions Python script. |
| **Secrets** | Google Secret Manager |  For auditing and rotation of sensitive data.|
| **Monitoring** | Google Cloud Monitoring and Cloud Trace | For creating dashboards and alerts to monitor application performance and health|



---

## Getting Started (Local)


###Start by installing the Google Cloud Command Line Interface (Instructions are listed below):

General Installation Steps:
Go to the Official Documentation: The best place to start is the official Google Cloud SDK documentation: https://cloud.google.com/sdk/docs/install
Choose Your Operating System: On the installation page, select your operating system (Windows, macOS, or Linux).
Follow the Specific Instructions:
Windows:
Google provides an installer executable (GoogleCloudSDKInstaller.exe). You'll download and run this installer, which guides you through the process. It often bundles a compatible Python version, which is a prerequisite.
After installation, it will typically offer to start a Google Cloud CLI shell and configure gcloud init.
macOS:
You can typically download an archive (.tar.gz file) and then run an installation script (install.sh) from within the extracted directory.
Alternatively, you can use brew if you have Homebrew installed: brew install --cask google-cloud-sdk.
Linux:
Package Manager (Recommended for most distributions): Google provides repositories for popular Linux distributions (Debian/Ubuntu, Red Hat/CentOS/Fedora). This is often the easiest method as it allows for easy updates using your system's package manager (apt, dnf, yum). You'll add Google's repository, import the GPG key, and then install google-cloud-cli using your package manager.
Archive Method: Similar to macOS, you can download a .tar.gz archive, extract it, and run an install.sh script. You'll then need to manually add the SDK to your PATH and enable shell command completion.
Initialize the gcloud CLI (gcloud init):
After the initial installation, you'll almost always need to run gcloud init. This command will:
Walk you through authenticating with your Google Cloud account.
Help you select or create a Google Cloud project to work with.
Optionally configure a default compute region and zone.
You'll be prompted to open a URL in your browser to complete the authentication process.
Important Considerations for the Google Cloud CLI:
Python: The Google Cloud CLI requires Python. The Windows installer often bundles it. For Linux and macOS, ensure you have a supported Python version installed (usually Python 3.9 to 3.13 are supported).
Updates: Regularly update your gcloud CLI to get the latest features and bug fixes: gcloud components update.
Proxy Settings: If you are behind a corporate proxy, you might need to configure proxy settings for the gcloud CLI. The documentation has instructions for this.
Permissions: Ensure your user account has the necessary permissions on your local machine to perform the installation. You might need administrator or sudo privileges.
### Set up Region and Zone for the Food-Holiday Project
For this project, I am configuring my region to be us-east 1 and my zone to us-east1-b.  Within the terminal, I entered the following
gcloud config set compute/region us-east1
gcloud config set compute/zone us-east1-b


Results:


###Enable all API’s Needed for Project
Next, we have to activate all of the necessary API’s for this project 
Cloud Functions API
Cloud Build API
Cloud Logging API
Cloud Monitoring API
Secret Manager API 
Enter in the CLI the following script:
gcloud services enable cloudfunctions.googleapis.com \
                       cloudbuild.googleapis.com \
                       sourcerepo.googleapis.com \
                       logging.googleapis.com \
                       monitoring.googleapis.com \
                       secretmanager.googleapis.com


Output:
Operation "operations/acf.p2-647488352163-dccd6a18-9022-4a09-8592-bf9a4e069c62" finished successfully.



All of the API’s needed for this project are now loaded and ready for use case
### Setting up Secrets Manager

This particular secret sets up the email addresses of the Sender and the receiver. I want this information to be private and not exposed to the public internet (Github Repository as well) for security reasons. 





##Configuration & Secrets


Key
Description
Source / Location
SENDER_EMAIL_ADDRESS
Sender’s Email Address
Secret Manager

SENDER_EMAIL_PASSWORD
Sender’s Email Password
Secret Manager





RECIPIENT_EMAILS
Email Address(es) that will receive the output of this function
Secret Manager

## Observability
Dashboards: Google Cloud Monitoring will be used to create custom dashboards visualizing Cloud Function invocations, execution times, and error rates.

Logs: Cloud Function logs will be streamed to Google Cloud Logging for detailed debugging and auditing.

Alerts: Alerts will be configured in Cloud Monitoring to notify relevant personnel (e.g., via email or Slack) on critical errors, excessive invocations, or function failures.

SLOs (Service Level Objectives):Once a day @ 8AM, Each and Every Day



##Security & Compliance
A dedicated Service Account has been created for this GCP Project. Specific IAM Roles will be assigned to this service account following the principle of least privilege access, ensuring it only has the necessary permissions to execute the Cloud Function and access Secret Manager.

##Cost & Resource Estimates

This application is designed to qualify for the GCP Free Tier, as it will be called less than 100 times a month. A conservative budget of $5 per month will be allocated to cover any unforeseen costs or minor overages.

##Roadmap / Future Work
Beautify Visuals: Enhance the email notification's visual presentation for a more engaging user experience.

Incorporate More Information: Expand the application to include additional relevant data, such as:

Stock market data
Weather forecasts

Containerization: Containerize this application using Docker and potentially deploy it to Cloud Run for greater portability and scalability options.


