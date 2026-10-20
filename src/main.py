# Copyright (c) Microsoft. All rights reserved.

import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient,FoundryToolbox,StoreProvider
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
#from azure.monitor.opentelemetry import configure_azure_monitor
# Load environment variables from .env file
load_dotenv()




def main():
    model_name = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME") or os.getenv("FOUNDRY_MODEL_NAME")
    if not model_name:
        raise RuntimeError(
            "Model deployment name is not configured. Set "
            "AZURE_AI_MODEL_DEPLOYMENT_NAME or FOUNDRY_MODEL_NAME."
        )



    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=model_name,
        credential=DefaultAzureCredential(),
    )



    

   

    
    agent = Agent(
        client=client,
        instructions="You are a friendly assistant. Keep your answers brief.",
        # History will be managed by the hosting infrastructure, thus there
        # is no need to store history by the service. Learn more at:
        # https://developers.openai.com/api/reference/resources/responses/methods/create
        default_options={"store": True},
    )

    

    server = ResponsesHostServer(agent)
    server.run()


if __name__ == "__main__":
    main()
