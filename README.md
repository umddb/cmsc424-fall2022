## Brief Setup Instructions 

There are more detailed setup instructions in `Assignment-0` and the other directories.

1. Clone the GitHub Class Repository to get started (there are more detailed instructions in `Assignment-0` README):
`git clone https://github.com/umddb/cmsc424-fall2022.git`

1. You can load the systems directly on your machines (easier on Linux or Mac), but to make things easier, we have provided a Docker Image with
PostgreSQL pre-loaded (we will update the image throughout the semester).
    - Install Docker Desktop: https://www.docker.com/products/docker-desktop
    - Run the docker image: `docker run --rm -ti -p 8888:8888 -p 8881:8881 -p 5432:5432 -v /Users/amol/git/cmsc424-fall2022:/data amolumd/cmsc424-fall2022`. Make sure
    to replace "/Users/amol/..." with the correct path of the `top level directory` in the cloned GitHub repository. 
    - Assuming it ran successfully, you should be logged in as `root` in the docker container, and you should see the shell.
    - The above command maps three ports on the virtual machine: 8888, 8881, and 5432 (PostgreSQL). This means that if you go to 'http://127.0.0.1:8888', you will
    actually be connecting to the 8888 port on the virtual machine (on which we are running the Jupyter Notebook). However, if your computer is already using these
    ports, you will have to modify those. 
    - The above command also mounts the local GitHub directory into `/data` on the virtual machine. Do `ls /data` in the virtual machine to confirm that you can see
    `Assignment-0` directory in there.
    - NOTE: you will be logged in as `root`.
    - At this point, you should be able to use psql: `psql university`
    - Jupyter Notebook should be pre-started (try http://127.0.0.1:8888), but if not, you can do: `jupyter-notebook --port=8888 --allow-root --no-browser --ip=0.0.0.0`
    - As soon as you exit the Docker container, the machine will shut down -- so only changes you have made in the /data directory will persist.

1. *If you are having trouble installing Docker or somewhere in the steps above, you can also install the software directly by going through the commands listed in
the Dockerfile*


## Important: Read before Visiting Office Hours for Errors

1. If you run into issues installing Docker Desktop, do Google searches on the errors to see if there are any instructions to fix those. That's what we would do if you
come to office hours. 

1. If you run into issues running the docker image (using `docker run`), post a screenshot of the error in Piazza. The most likely error I can imagine is port mapping.
For example, if it complains that port 8888 is already used, then just modify the above command to use `-p 8889:8888` instead. If that works, then to use Jupyter
notebook, you would have to go to: http://127.0.0.1:8889 instead of the link provided above.

1. Assuming no errors in running docker image, I am not sure why either PostgreSQL or Jupyter Notebook wouldn't work, but we will update this section if we see more
errors.
