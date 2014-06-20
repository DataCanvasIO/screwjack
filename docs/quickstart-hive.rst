====================================
Getting Started with Screwjack(Hive)
====================================

This is a show case for the usage of screwjack hive runtime. This
section we will create a EMR hive module to get the topN hot tokens in
search queries.

At first, thanks AOL share their query log online [1]_. We download a
piece of them from http://www.infochimps.com/datasets/aol-search-data as
the test data in this demo. The data looks like below:

::

        AnonID  Query   QueryTime   ItemRank    ClickURL
        142 rentdirect.com  2006-03-01 07:17:12     
        142 www.prescriptionfortime.com 2006-03-12 12:31:06     
        142 staple.com  2006-03-17 21:19:29     
        142 staple.com  2006-03-17 21:19:45     
        142 www.newyorklawyersite.com   2006-03-18 08:02:58     
        142 www.newyorklawyersite.com   2006-03-18 08:03:09     
        142 westchester.gov 2006-03-20 03:55:57 1   http://www.westchestergov.com
        142 space.comhttp   2006-03-24 20:51:24     
        142 dfdf    2006-03-24 22:23:07     
        142 dfdf    2006-03-24 22:23:14     
        142 vaniqa.comh 2006-03-25 23:27:12     
        142 www.collegeucla.edu 2006-04-03 21:12:14     
        142 www.elaorg  2006-04-03 21:25:20     
        142 207 ad2d 530    2006-04-08 01:31:04     
        142 207 ad2d 530    2006-04-08 01:31:14 1   http://www.courts.state.ny.us
        142 broadway.vera.org   2006-04-08 08:38:23     
        142 broadway.vera.org   2006-04-08 08:38:31     
        142 vera.org    2006-04-08 08:38:42 1   http://www.vera.org
        142 broadway.vera.org   2006-04-08 08:39:30     
        142 frankmellace.com    2006-04-09 02:19:24     
        142 ucs.ljx.com 2006-04-09 02:20:44     
        142 attornyleslie.com   2006-04-13 00:25:27     
        142 merit release appearance    2006-04-22 23:51:18     
        ............................

Step 0: Initialize a hive module
================================

.. code:: bash

    screwjack init emr_hive -n hot_token_topN_on_emr -d "Get hotest token in search engine query log."

When prompt for ``Module Version`` and other options, you can press
ENTER to use default options.

::

    Module Version [0.1]: 
    Module Entry Command [/usr/bin/python main.py]: 
    Base Image [zetdata/ubuntu:trusty]: 
    init emr_hive
    Sucessfully created 'hot_token_topn_on_emr'

After that, you will get a directory which its name is
``hot_token_topn_on_emr``.

Step 1: Add the input/output and parameter to this module.
==========================================================

.. code:: bash

    screwjack input_add query_log_s3_dir hive.s3.id_query_querytime
    screwjack output_add hot_token_topN_s3_dir hive.s3.table.token_count
    screwjack param_add topN string

Here ``query_log_dir`` is the hdfs dirctory which contain the raw data.
The schema of the data is id,query and querytime. The ``hot_token_topN``
is the hive table name we gonna dump our result in.

Step 2: (optional) Make the UDF help explore the query into tokens
==================================================================

This step is optional. When you want a UDF in your module. Here is a
example at:
`example-modules <https://github.com/DataCanvasIO/example-modules/tree/master/tutorials/emr_hive/udft>`__.
After you build the jar of your UDF, you should put it into
``./resource/udfs``. Then, the HiveRuntime can automatically upload
files s3.

Step 3: Write the hive script.
==============================

Then, we can open ``main.hql`` to fill our code like this:

.. code:: text


      set hive.base.inputformat=org.apache.hadoop.hive.ql.io.HiveInputFormat;

      CREATE TEMPORARY FUNCTION splitword AS 'com.your_company.hive.udtf.SplitWord';

      --CREATE OUTPUT TABLE

      DROP TABLE IF EXISTS hot_token_topN_table;
      CREATE EXTERNAL  TABLE hot_token_topN_table
      (
              token STRING,
              freq  INT
      )
      ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
      LINES TERMINATED BY '\n'
      STORED AS TEXTFILE LOCATION '${OUTPUT_hot_token_topN_s3_dir}';

      --CREATE AN EXTERNAL TABLE TO LOAD THE QUERY DATA
      DROP TABLE IF EXISTS query;
      CREATE EXTERNAL TABLE query
      (
              id STRING,
              site STRING,
              timestp TIMESTAMP
      )
      ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
      LINES TERMINATED BY '\n'
      LOCATION '${INPUT_query_log_dir_s3_dir}';

      INSERT OVERWRITE TABLE hot_token_topN_table
      SELECT token, freq FROM
      (
              SELECT token,count(1) AS freq FROM
              (
                      SELECT splitword(site) AS token FROM query
              )token_table
              GROUP BY token
      )token_frep
      ORDER BY freq DESC LIMIT ${PARAM_topN};

You could reference the input parameter defined with screwjack by
``${INPUT_inputname}``, such as ``${INPUT_query_log_s3_dir}`` in this
case. Output parameter by ``${OUTPUT_outputname}``, such as
``${OUTPUT_hot_token_topN_s3_dir}`` in this case. Parameter by
``${PARAM_paramname}``, such as ``${PARAM_topN}`` in this case.

Step 4: Test locally
====================

Before test, we need to upload the sample data to S3. Here we put them
on ``s3://get-hot-token-kk/input/query``. As module take input from its
precursor, when we do test, we need to feed it by ourself. We touch the
input parameter file and output parameter file to contain the input
parameter and the output result. In this case, our input parameter is
the s3 directory which contains the query logs. So create the file
``./input.param`` and write ``s3://get-hot-token-kk/input/query`` into.
Then create an output param to recive the output.

.. code:: bash

    screwjack run local

Then type the corresponding parameter to run the test.

::

        Param 'FILE_DIR' [./resources/files]:
        Param 'UDF_DIR' [./resources/udfs]:
        Param 'AWS_ACCESS_KEY_ID' []: YOUR_AWS_ACCESS_KEY
        Param 'AWS_ACCESS_KEY_SECRET' []: YOUR_AWS_ACCESS_KEY_SECRET
        Param 'S3_BUCKET' []: get-hot-token-kk
        Param 'AWS_Region' []: us-east-1
        Param 'EMR_jobFlowId' []: YOUR_EMR_JOB_FLOW_ID
        Param 'topN' []: 10
        Input 'query_log_s3_dir': input.param
        Output 'hot_token_topN_s3_dir': output.param

During the test, if any error or bug emerge, you could modfiy your udtf
and hive script according to the propted log. If everything is ok, the
defined output parameter will be created and written into the
``output.param``. If the test finished successfully, we could get the a
s3 directory in output.param. Here we get
``s3://get-hot-token-kk/zetjob/your_username/job456/blk789/OUTPUT_hot_token_topN_s3_dir``.
Let us open the file on s3 and we get the hotest 10 tokens among the
query.

::

        of,110575
        -,104052
        in,91521
        the,82961
        for,70107
        and,66675
        to,45168
        free,45149
        a,36220
        google,34970

Step 5: Test in docker
======================

.. code:: bash

    screwjack run docker

This step is to test whether the module could correctly run in a docker
image. At first, screwjack will help to build a specific image with a
hive runtime in. Then it will test your script and udfs in this image.
If it turns out to be a success, we get this module ready to run online.

.. [1]
   G. Pass, A. Chowdhury, C. Torgeson, "A Picture of Search" The First
   International Conference on Scalable Information Systems, Hong Kong,
   June, 2006.
