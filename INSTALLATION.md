2019.04.07
This is a very rough start of installation instructions - mostly notes to be organized later.

AWS instance definitions are located in the `pegasus` directory, and use the `pegasus`
configuration management tool from Insight Data Science.

Configuration files for each instance (or instance group) are defined in `.yaml` files, 
which includes information regarding the subnet, security group, and reference to my 
PEM key.  It might not be appropriate to push these to a public repository.  

```
git clone https://github.com/InsightDataScience/pegasus.git

cd pegasus
```

```
git clone https://github.com/simchuck/InsightDataEngineering.git
```

May have to copy files from my project sub-directory into the pegasus directory for the
pegasus scripts to run properly.

Edit the `.yaml` files as appropriate.
Edit the `.config` files as appropriate with your information.
The `start_XXX.sh` files should be okay -- defining all of the necessary installations
and configurations necessary on each instance for the correct infrastructure.
Run the `start_demo.sh` script to spin-up the demo.


