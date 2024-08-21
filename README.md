# SaaS Bot System
The SaaS Bot System is a powerful application designed to facilitate interactions between clients and users through advanced AI-driven bots. Built with FastAPI, Python, and Poetry, this system allows clients to train models based on their websites and provides users with multiple bots to interact with.

## Features
Client Integration: Clients can submit their website links to train a model based on their site’s content.
User Interaction: Users can select from multiple bots and engage in conversations with them.
Bot Management: Easily manage and deploy various bots for different use cases.
Real-time Responses: Experience responsive and accurate interactions with the AI bots.

## Technology Stack
Backend: FastAPI
Dependency Management: Poetry

## Installation
To set up the SaaS Bot System on your local machine, follow these steps:

1.**Clone the Repository:**
```bash
git clone https://github.com/sarohy03/RAG-llm/tree/my-recovery-branch 
cd RAG-llm
```
2 **Install Dependencies with Poetry:**
```bash 
poetry install
```
This will install all required dependencies listed in the pyproject.toml file.

3. **Activate the Poetry Environment:**
```bash
poetry shell
```
4. **Run the Development Server:**

```bash
poetry run uvicorn main:app --reload
```
The server will run at http://127.0.0.1:8000/.

## Usage

- **Client Interaction:** Clients can submit their website URLs through the provided endpoint to initiate the model training process.
- **User Interaction:** Users can access the bot selection interface and start conversations with their chosen bot.
- **Bot Management:** Use the provided admin tools to manage and configure bots.
Future Enhancements
- **Advanced Bot Features:** Implement more sophisticated AI capabilities and enhance bot interactions.
- **Analytics Dashboard:** Develop a dashboard for clients to view detailed analytics on bot performance and user interactions.
- **Mobile Support:** Create a mobile-friendly interface for both clients and users.

## Work Flow 
- At first a Client signs up to our site then logs in 
- After that Cient create the bot 
- At this step the context from website is retrived and saved in data base 
- After that user logs in 
- He selects a bot and uses it 
- When the user send query the data system perform vector search locally and find the most relevent piece of data 
- After that the data is processed by LLM and returns the results
