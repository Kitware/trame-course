# Cloud deployment example

This repository provide a simple example on how to deploy a single file trame application onto a CapRover instance using the git approach.

## Background

When creating a single file application with trame the only files that you need to edit for your specific needs are:
- `app.py`: Should contain your own application code with a `__main__` section
- `./setup/requirements.txt`: Should list all your dependencies including `trame`
- `./setup/apps.yaml`: Should add any additional args/parameters you may need for your app. Or list all the app you want to deploy at once.

Generic file that don't needs edits:
- `Dockerfile`: contains the basic multi-user setup for trame apps.
- `captain-definition` Point to the dockerfile for building the deployment.

## CapRover endpoint setup

Within the CapRover web interface, for your application make sure you enable `"WebSocket Support"` at the bottom of the `"HTTP Settings"` page. 

Then ideally you should also __Enable HTTPS__ and check __Force HTTPS by redirecting all HTTP traffic to HTTPS__

## How to deploy

The idea is to rely directly on git so in order to deploy such repository, you should be able to run the following command lines:

```bash
git clone https://github.com/Kitware/trame-app-cone.git
cd trame-app-cone
caprover deploy
```

Then follow the flow of the questions to finish the deployment.

```bash
Preparing deployment to CapRover...

? select the CapRover machine name you want to deploy to: xyz
Ensuring authentication...
? CapRover machine password: [hidden]
? select the app name you want to deploy to: cone
? git branch name to be deployed: main
? note that uncommitted and gitignored files (if any) will not be pushed to server! Are you sure you want to deploy? Yes

Saving tar file to: ".../temporary-captain-to-deploy.tar"
Using last commit on "main": 2bf332cbc589b50d03e58b17b71be2415a6ff250

Deploying cone to xyz...

Uploading [====================] 100%  (ETA 0.0s)
Upload done.

This might take several minutes. PLEASE BE PATIENT...

Building your source code...

------------------------- Thu Nov 10 2022 01:41:49 GMT+0000 (Coordinated Universal Time)
Build started for cone
Ignore warnings for unconsumed build-args if there is any
Step 1/3 : FROM kitware/trame

---> e74b197b974f
Step 2/3 : COPY --chown=trame-user:trame-user . /deploy

---> Using cache
---> 85dcdd452f2e
Step 3/3 : RUN export TRAME_BUILD_ONLY=1 && /opt/trame/entrypoint.sh

---> Using cache
---> 23f30b5ae59d
[Warning] One or more build-args [CAPROVER_GIT_COMMIT_SHA] were not consumed
Successfully built 23f30b5ae59d
Successfully tagged img-captain-cone:latest
Build has finished successfully!

Deployed successfully cone
App is available at https://cone.xyz...
```

And that's it...
