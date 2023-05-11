## Setup

Original information from https://github.com/Kitware/trame-ondemand-bc-cone

```bash
git clone https://github.com/ubccr/hpc-toolset-tutorial.git
cd hpc-toolset-tutorial
./hpcts start
```

For mac Arm you will need to add `yum install python3-devel` onto `frontend`, `cpn01`, `cpn02` by running the following commands

```bash
docker exec -it -u 0 cpn01 bash
  yum install python3-devel

docker exec -it -u 0 cpn02 bash
  yum install python3-devel

docker exec -it -u 0 frontend bash
  yum install python3-devel
```

open `https://localhost:3443/` then

- login: `hpcadmin`
- password: `ilovelinux`

From the Open OnDemand Dashboard, click "Develop"->"My Sandbox Apps (Development)".

1. Click "New App"
2. Clone Existing App

  - Directory Name: `trame-example`
  - Git remote: `https://github.com/kitware/trame-ondemand-bc-cone`
  - Click `Submit`


## Run

Go to "Develop"->"My Sandbox Apps (Development)" and click the "Launch Trame App" button.
