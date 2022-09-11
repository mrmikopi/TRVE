import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions.{monotonically_increasing_id, row_number, rand}
import org.apache.spark.sql.types.{StructType, StructField, StringType};
import org.apache.spark.sql.{Row, DataFrame};
import java.io._;
import scala.collection.mutable.ListBuffer;

object DataExtraction {

  def getMadPlus() : DataFrame = {

    // get file names. TODO : Input olarak?
    var files = new File("/home/kaan/Repos/metal_dataset/").list   

    /* create mad+ */
    // create schema
    val schema = StructType(
    StructField("band_name", StringType, true) ::
    StructField("mad_genre", StringType, false) :: Nil)

    // create dataframe
    var madPlus = spark.createDataFrame(spark.sparkContext.emptyRDD[Row], schema)
    var tempDf = spark.createDataFrame(sc.emptyRDD[Row], schema)

    /* File Iteration */
    // Create temp list for band files
    var bandFiles = new ListBuffer[String]()

    // Iterate through Files
    for
      (i <- files)
      {
        val splitStr = i.split("_");
        val arrSize = splitStr.size;
        if
          (splitStr.last == "bands.txt")
          {
            var genreName : String = "";
            for (word <- splitStr.slice(0, arrSize - 1))
              {
                // Get full genre name for this file
                if (genreName == "") 
                   (genreName += word)
                else (genreName = genreName + " " + word)
              }

            // Read from current file to DataFrame
            val bandNames = spark.read.text("/home/kaan/Repos/metal_dataset/" + i)
            // Add genre name to all columns
            val bandsWithGenre = bandNames.withColumn("mad_genre", lit(genreName))
            // Union dataframes
            madPlus = madPlus.union(bandsWithGenre)
          }
      }

      println("Band name processing finished. Details for Dataframe:")
      madPlus.describe().show()
      val sampleCount = 50;
      println(sampleCount + " sample rows for you metalheads \\m/")
      madPlus.sample( 1.0 * sampleCount / madPlus.count()).show(sampleCount)

      return madPlus;
  }

  // Util Method for project name ideas :)
  def getTrveNames(df : DataFrame) : DataFrame = {

    val schema = StructType(
    StructField("word", StringType, true) ::
    StructField("start_letter", StringType, false) :: Nil)
    
    var keywords = spark.createDataFrame(spark.sparkContext.emptyRDD[Row], schema)

    // TODO Her kelimeyi ayri bir row olarak ekle
    
    // Yaptigim shell denemesi:
    // val dfWords = df.select(split(col("band_names"),"[. ,-_;:/\\]").as("words")).drop("band_name")

    // temp view
    //df.createGlobalTempView("bands")

    // Index column for dfWords
    // dfWords = dfWords.withColumn("row_index", 
    //   row_number().over(
    //       Window.orderBy(monotonically_increasing_id())))

    // TODO t r v e olan kolonlari filtrele
    //var tempDf = df.filter(df("band_name").startsWith()).show(false)

    return keywords;
  }

  def getRandomTrve() : DataFrame = {
    
    // TODO Buraya dfT'leri olusturdugun scripti ekleyebilirsin belki
    
    val windowSpec = Window.partitionBy("word").orderBy("word")
    
    // TODO Asagidaki path'ler degismeli.
    var dfT = spark.read.csv("/home/kaan/Repos/TRVE/deneme/dfT.csv").withColumnRenamed("_c0","word")
    var dfR = spark.read.csv("/home/kaan/Repos/TRVE/deneme/dfR.csv").withColumnRenamed("_c0","word")
    var dfV = spark.read.csv("/home/kaan/Repos/TRVE/deneme/dfV.csv").withColumnRenamed("_c0","word")
    var dfE = spark.read.csv("/home/kaan/Repos/TRVE/deneme/dfE.csv").withColumnRenamed("_c0","word")
    
    dfT = dfT.orderBy(rand()).limit(1)    
    dfR = dfR.orderBy(rand()).limit(1)    
    dfV = dfV.orderBy(rand()).limit(1)    
    dfE = dfE.orderBy(rand()).limit(1)    

    // dfT = dfT.sample(1.0/dfT.count()).limit(1)
    // dfR = dfR.sample(1.0/dfR.count()).limit(1)
    // dfV = dfV.sample(1.0/dfV.count()).limit(1)
    // dfE = dfE.sample(1.0/dfE.count()).limit(1)

    dfT = dfT.withColumn("row_index", lit(1))
    dfR = dfR.withColumn("row_index", lit(1))
    dfV = dfV.withColumn("row_index", lit(1))
    dfE = dfE.withColumn("row_index", lit(1))

    dfT.show()
    dfR.show()
    dfV.show()
    dfE.show()

    dfT = dfT.join(dfR,dfT("row_index") === dfR("row_index"),"inner" )
      .join(dfV,dfT("row_index") === dfV("row_index"),"inner")
      .join(dfE,dfT("row_index") === dfE("row_index"),"inner")
              
    dfT.show()
    return dfT

  }
}
