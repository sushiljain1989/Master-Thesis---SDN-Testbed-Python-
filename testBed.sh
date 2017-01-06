#!/bin/bash
TESTBEDHOME="$HOME/testbed"
PYRETICHOME="$HOME/pyretic"
startMininet()
{
    
     echo -e "Running mininet \n"
     sudo -E python $TESTBEDHOME/Simple_Pkt.py 127.0.0.1 6633 > $TESTBEDHOME/logs/mininet_$1.out
}
killMininet()
{
    echo -e "Clearing Mininet configuration \n"
    sudo mn -c
}
runApplication()
{
    if [ "frenetic" == "$1" ]
        then
            runController "$1"
            nohup python $TESTBEDHOME/frenetic_app.py > $TESTBEDHOME/logs/app_frenetic.out&
    elif [ "pyretic" == "$1" ]
        then
            echo -e "********Preparing Pyretic controller with application*********\n"
            echo -e "Copying application to Pyretic modules directory\n"
            cp $TESTBEDHOME/pyretic_app.* $PYRETICHOME/pyretic/modules/
            echo -e "Changing directory to Pyretic Home\n"
            cd $PYRETICHOME
            echo -e "Running Pyretic controller with application\n"
            nohup pyretic.py -m p0 pyretic.modules.pyretic_app > $TESTBEDHOME/logs/controller_and_app_pyretic.out&
            
    
elif [ "kinetic" == "$1" ]
        then
            echo -e "********Preparing Kinetic controller with application*********\n"
            echo -e "Copying application to Kinetic app directory\n"
            cp $TESTBEDHOME/kinetic_app.* $PYRETICHOME/pyretic/kinetic/apps/
            echo -e "Changing directory to Pyretic Home\n"
            cd $PYRETICHOME
            export KINETICPATH=$HOME/pyretic/pyretic/kinetic
            nohup pyretic.py -m p0 pyretic.kinetic.apps.kinetic_app > $TESTBEDHOME/logs/controller_and_app_kinetic.out&
            
            
    fi
    sleep 10

}
killApplication()
{
    echo -e "Killing $1 \n"
    if [ "frenetic" == "$1" ]
        then
        killController "$1"
        kill -9 $(lsof -i:41414) 2> /dev/null

    elif [ "pyretic" == "$1" ]
         then
         kill -9 $(lsof -i:6633) 2> /dev/null
         kill -9 $(lsof -i:41414) 2> /dev/null
    elif [ "kinetic" == "$1" ]
         then
         kill -9 $(lsof -i:6633) 2> /dev/null
         kill -9 $(lsof -i:41414) 2> /dev/null
    fi

    sleep 5
}
runController()
{
    echo -e "Running frenetic controller\n"
    nohup frenetic http-controller --verbosity debug > $TESTBEDHOME/logs/controller_frenetic.out&
    CPID=$!
    
}
killController()
{
    if [ "frenetic" == "$1" ] 
        then
            echo -e "Killing $1 controller\n"
            kill -9 $(lsof -i:6633) 2> /dev/null
            kill -9 $(lsof -i:9000) 2> /dev/null
            kill -9 $(lsof -i:8984) 2> /dev/null
    fi

}
if [ "$1" == "-h" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "--help" ]
then
        echo "Usage : testBed.sh -a (application) application_name"
        echo "                   -c (controller[s]) list of comma separated controllers"
        echo "                   -m (mininet) mininet topology file"


        exit 0
fi

if [ "$1" == "-a" ] || [ "$1" == "-A" ] && [ "$3" == "-c" ] && [ "$5" == "-m" ]
    then
        IFS=', ' read -r -a array <<< "$4"

        for element in "${array[@]}"
            do
                if [ "$element" == "frenetic" ]
                    then
                        
                        runApplication "$element"
                        startMininet "$element"
                        killApplication "$element"
                        killMininet
                        sleep 5


                elif [ "$element" == "pyretic" ]
                    then
                        runApplication "$element"
                        startMininet "$element"
                        killApplication "$element"
                        killMininet
                        sleep 5

                elif [ "$element" == "kinetic" ]
                    then
                       
                        runApplication "$element"
                        startMininet "$element"
                        killApplication "$element"
                        killMininet
                        sleep 5

                fi

            done


fi
echo -e "====================\n"