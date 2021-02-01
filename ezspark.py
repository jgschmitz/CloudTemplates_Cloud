## Running Spark 3.4.4+ in Standalone mode
 
Try Installing with Brew, this makes the life easy.
- Open your command line, if you have brew
      - update brew
  if you don't have brew,
      - Install brew, copy and paste the below command (Avialable at (http://brew.sh/))
      /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
       
- Install Hadoop , spark uses yarn resources and this is essentials 
       -> brew install hadoop 
  sometimes this will through an error if your system doesn't have java, cool thing about brew is it provides a command to 
  install java, run that command and java gets installed.
   
- Install spark 
      -> brew install apache-spark 
       
Success: Spark got installed. 
run pyspark on command line and you should see the spark running 
print 1,2,3,4,4,5,6
 
## Connecting ipython to spark 
 
I haven't followed the above process for working with spark on ipython notebook . I have uninstalled everything I have done 
before and worked on the following lines 
 
- Open the link (http://spark.apache.org/downloads.html) and download it in the folder you wish (in my case it is ~/Downloads)
- Go to the command line and execute the following the statements 
      *  tar xvzf spark-2.0.1-bin-hadoop2.7.tgz (unzip the downloaded folder )
      *  mv spark-2.0.1-bin-hadoop2.7 spark2 (change the filename to spark2)
      *  cd spark2/sbin (go to the sbin folder)
      * ./start-master.sh (open the start-master.sh file. This will start the spark 
      * cd ../logs
      * ls (should show you a link)
      * tail link(as given above)(this will show you that spark as started and give you web link to check the spark 
 
- In the command line 
      * pip install findspark (More about it https://github.com/minrk/findspark)
   
- In the ipython notebook 
     * import findspark 
     * findspark.init("/Users/Satish/Downloads/spark2/")
     * import pyspark 
     * from pyspark.sql import DataFrameNaFunctions 
     * from pyspark.sql.functions import lit 
     * from pyspark.ml.feature import StringIndexer #label encoding
     * from pyspark.ml import Pipeline
     * sc = pyspark.SparkContext(appName="helloworld")
