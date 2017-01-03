
#!/bin/bash
TESTBEDHOME="$HOME/testbed"
PYRETICHOME="$HOME/pyretic"
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
                        echo -e "Running frenetic controller\n"
                        nohup frenetic http-controller --verbosity debug > $TESTBEDHOME/logs/controller_frenetic.out&
            CPID=$!
                        sleep 10
                        echo -e "Running application for controller\n"
                        nohup python $TESTBEDHOME/frenetic_app.py > $TESTBEDHOME/logs/app_frenetic.out&
                        APID=$!
                sleep 5
                        echo -e "Running mininet \n"
                        sudo -E python $TESTBEDHOME/Simple_Pkt.py 127.0.0.1 6633 > $TESTBEDHOME/logs/mininet_frenetic.out
                        echo -e "Killing frenetic controller\n"
                        kill -9 $CPID
                        sleep 5
                        echo -e "Killing frenetic app\n"
                        kill -9 $APID
                        kill -9 $(lsof -i:6633) 2> /dev/null
            kill -9 $(lsof -i:41414) 2> /dev/null
            echo -e "Clearing Mininet configuration \n"
                        sudo mn -c
            sleep 5
                                

                elif [ "$element" == "pyretic" ]
                    then
                        echo -e "Running Pyretic controller with application\n"
                        cp $TESTBEDHOME/pyretic_app.* $PYRETICHOME/pyretic/modules/
                        cd $PYRETICHOME
                        nohup pyretic.py -m p0 pyretic.modules.pyretic_app > $TESTBEDHOME/logs/controller_and_app_pyretic.out&
                        CPID=$!
                        sleep 10
                       
                        echo -e "Running mininet \n"
                        sudo -E python $TESTBEDHOME/Simple_Pkt.py 127.0.0.1 6633 > $TESTBEDHOME/logs/mininet_pyretic.out
                        echo -e "Killing pyretic controller and application\n"
                        kill -9 $CPID
            kill -9 $(lsof -i:6633) 2> /dev/null
            kill -9 $(lsof -i:41414) 2> /dev/null
                        sleep 5
                        echo -e "Clearing Mininet configuration \n"
                        sudo mn -c
                        sleep 5
        elif [ "$element" == "kinetic" ]
            then
                        echo -e "Running kinetic(pyretic) controller with application\n"
                        cp $TESTBEDHOME/kinetic_app.* $PYRETICHOME/pyretic/kinetic/apps/
                        cd $PYRETICHOME
            export KINETICPATH=$HOME/pyretic/pyretic/kinetic
                        nohup pyretic.py -m p0 pyretic.kinetic.apps.kinetic_app > $TESTBEDHOME/logs/controller_and_app_kinetic.out&
                        CPID=$!
                        sleep 10

                        echo -e "Running mininet \n"
                        sudo -E python $TESTBEDHOME/Simple_Pkt.py 127.0.0.1 6633 > $TESTBEDHOME/logs/mininet_kinetic.out
                        echo -e "Killing kinetic(pyretic) controller and application\n"
                        kill -9 $CPID
                        kill -9 $(lsof -i:6633) 2> /dev/null
                        kill -9 $(lsof -i:41414) 2> /dev/null
            sleep 5
                        echo -e "Clearing Mininet configuration \n"
                        sudo mn -c
                        sleep 5

                fi

            done


fi
echo -e "====================\n"


