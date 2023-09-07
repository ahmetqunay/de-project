#gerekli kutuphaneleri ice aktar
from pyspark.sql.functions import from_json 
from pyspark.sql.types import StructType, StructField, StringType, FloatType, DateType, IntegerType

# sparki google'a bagla !bucket name i degistir
bucket = "us-bucket-de"
spark.conf.set("temporaryGcsBucket", bucket)
spark.conf.set("parentProject", "caramel-slice-395008")

#kafkadan veriyi oku !kafka ip sini degistir
kafka_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "35.227.180.82:9092") \ 
    .option("subscribe", "stocks") \ 
    .load()

#schema olustur !semayi yapilandir
schema = StructType([
    StructField("firma", StringType()),
    StructField("acilis", FloatType()),
    StructField("en_yuksek", FloatType()),
    StructField("en_dusuk", FloatType()),
    StructField("kapanis", FloatType()),
    StructField("hacim", IntegerType()),
    StructField("tarih", DateType()),
])

#verilere hizli erisebilmek icin kafka ile gelen veriyi semaya uyarla
activation_df = kafka_df.select(
    from_json(kafka_df["value"].cast("string"), schema).alias("activation")
)

#df degiskeninde istenen verileri sec
df = activation_df.select(
    "activation.firma",
    "activation.acilis",
    "activation.en_yuksek",
    "activation.en_dusuk",
    "activation.kapanis",
    "activation.hacim",
    "activation.tarih"
)

#verileri yapilandirdiktan sonra bigquerydeki tabloya yaz !tablo konumunu ini ve credential dosya konumunu degistir
modelcountquery = df.writeStream.outputMode("append") \ 
    .format("bigquery").option("table", "db.project1") \ 
    .option("checkpointLocation","/path/to/checkpoint/dir/in/hdfs") \
    .option("credentialsFile", "/home/fatihgunayapple/sa.json") \
    .option("truncate", False).start().awaitTermination()