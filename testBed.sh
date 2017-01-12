#!/bin/bash
TESTBEDHOME="$HOME/testbed"
PYRETICHOME="$HOME/pyretic"
OPENMULHOME="$HOME/openmul"
UPLOAD_DIR="/var/www/html/testbed/uploads/"
startMininet()
{
    local port=6633
     
    if [ "openmul" == "$1" ]
    then
        port=6653
    fi
     echo -e "Running mininet \n"
     sudo -E python $TESTBEDHOME/Simple_Pkt.py 127.0.0.1 "$port" > $TESTBEDHOME/logs/mininet_$1_$2.out
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
            nohup python $UPLOAD_DIR/$1/$2 > $TESTBEDHOME/logs/$1.out&
    elif [ "pyretic" == "$1" ]
        then
        #echo -e "$2" "$1"
        #exit 1
            echo -e "********Preparing Pyretic controller with application*********\n"
            echo -e "Copying application to Pyretic modules directory\n"
            cp $UPLOAD_DIR/$1/$2 $PYRETICHOME/pyretic/modules/
            echo -e "Changing directory to Pyretic Home\n"
            cd $PYRETICHOME
            echo -e "Running Pyretic controller with application\n"
        PYRETIC_NAME=`basename $2 .py`
        nohup pyretic.py -m p0 pyretic.modules.$PYRETIC_NAME > $TESTBEDHOME/logs/$1_and_$2.out&
            
    
    elif [ "kinetic" == "$1" ]
        then
            echo -e "********Preparing Kinetic controller with application*********\n"
            echo -e "Copying application to Kinetic app directory\n"
            cp $UPLOAD_DIR/$1/$2 $PYRETICHOME/pyretic/kinetic/apps/
            echo -e "Changing directory to Pyretic Home\n"
            cd $PYRETICHOME
            export KINETICPATH=$HOME/pyretic/pyretic/kinetic
        KINETIC_NAME=`basename $2 .py`
            nohup pyretic.py -m p0 pyretic.kinetic.apps.$KINETIC_NAME > $TESTBEDHOME/logs/$1_and_$2.out&
            
    elif [ "openmul" == "$1" ] 
    then
        echo -e "*******Preparing OpenMul controller************\n"
        echo -e "Copy application to OpenMUL Directory\n"
        sudo cp $UPLOAD_DIR/$1/$2 $OPENMULHOME/application/
        echo -e "Changing directory to OpenMul Home\n"
        cd $OPENMULHOME
        echo -e "Unzipping file...."
        cd $OPENMULHOME/application/
        sudo chmod 766 $2
        sudo unzip -o $2
        cd $OPENMULHOME
        runController "$1"
        NAME=`basename $2 .zip`
        echo -e "Running application"
        pwd
        sudo nohup ./application/$NAME/$NAME > $TESTBEDHOME/logs/$NAME.out&
        #exit 1 
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
    elif [ "openmul" == "$1" ]
     then
     cd $OPENMULHOME
     ./mul.sh stop
    fi
    sleep 5
}
runController()
{
   echo -e "Running $1 controller\n"
   
    if [ "frenetic" == "$1"  ]
    then
        nohup frenetic http-controller --verbosity debug > $TESTBEDHOME/logs/controller_$1.out&
        CPID=$!
    elif [ "openmul" == "$1" ]
    then
        cd $OPENMULHOME
        ./mul.sh start standalone > $TESTBEDHOME/logs/controller_$1.out&
    fi  
    
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
                        runApplication "$4" "$2"
                startMininet "$4" "$2"
                        killApplication "$4"
                        killMininet
                        sleep 5

fi
echo -e "====================\n"
