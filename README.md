## Background
More info here: https://coderecipe.ai/architectures/34142257

**Problem Statement:**

Build a simple but scalable chat room like [gitter](https://gitter.im) with default sentiment analysis that detects negative sentences.

**Solution:**

Leverage API Gateway's Websocket API to send and receive messages in real time without hosting a dedicated server, and [Google’s Natural Language API](https://cloud.google.com/natural-language/) to analyze sentiment of messages.

**Functional Requirements:**

Chatroom where multiple users can connect and chat in real time

Provide sentiment analysis for each chat

**Performance Requirements:**

Simultaneous connect with multiple users and send and receive multiple messages

Able to scale automatically without worry about setting up servers to maintain connections

**Assumptions:**

Assuming each users do not get to see the messages sent before they join

## prerequisites
Run the following commands from the `services/chatroom` folder:

npm install
pip install -r requirements.txt

## Deploy
Fill in the `services/chatroom/config.<stage>.json` file with the correct google cloud credentials which can be obtained from [here](https://cloud.google.com/docs/authentication/getting-started).
serverless deploy --stage <stage> --CONNECTIONS_TABLE <connections-table-name>