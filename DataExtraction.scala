import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions.{monotonically_increasing_id, row_number, rand}
import org.apache.spark.sql.types.{StructType, StructField, StringType};
import org.apache.spark.sql.{Row, DataFrame, Encoders};
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
      println(s"$sampleCount sample rows for you metalheads \\m/")
      madPlus.sample( 1.0 * sampleCount / madPlus.count()).show(sampleCount)

      return madPlus;
  }

  def getRandomTrve() : String = {
    
    // TODO Buraya dfT'leri olusturdugun scripti ekleyebilirsin belki:
    // SQL ile hallettim cogunu. her yere upper() yazmayi unutma. 
    // Split icin var dfWords = df.select(split(col("band_name"),"[. ,/]").as("words")) dene ama:
    // araya "-" da ekleyebiliyorsan ekle. Bazi grup isimlerinde var o.
    // Explode et.
    // monotonic id eklemen gerekirse 11.10.2022 notlarinda var. gerek olmayabilir sanki ayri ayri df'lere kaydederken.
    // Distinct sec dfT dfR olusturmak icin. Like 'T%' diyince okey olmasi lazim.
    
    val windowSpec = Window.partitionBy("word").orderBy("word")
    
    // TODO Asagidaki path'ler degismeli.
    var dfT = spark.read.csv("/home/kaan/Repos/TRVE/deneme/dfT.csv").withColumnRenamed("_c0","wordT")
    var dfR = spark.read.csv("/home/kaan/Repos/TRVE/deneme/dfR.csv").withColumnRenamed("_c0","wordR")
    var dfV = spark.read.csv("/home/kaan/Repos/TRVE/deneme/dfV.csv").withColumnRenamed("_c0","wordV")
    var dfE = spark.read.csv("/home/kaan/Repos/TRVE/deneme/dfE.csv").withColumnRenamed("_c0","wordE")
    
    dfT = dfT.orderBy(rand()).limit(1)    
    dfR = dfR.orderBy(rand()).limit(1)    
    dfV = dfV.orderBy(rand()).limit(1)    
    dfE = dfE.orderBy(rand()).limit(1)    

    dfT = dfT.withColumn("row_index", lit(1))
    dfR = dfR.withColumn("row_index", lit(1))
    dfV = dfV.withColumn("row_index", lit(1))
    dfE = dfE.withColumn("row_index", lit(1))

    dfT = dfT.join(dfR,dfT("row_index") === dfR("row_index"),"inner" )
      .join(dfV,dfT("row_index") === dfV("row_index"),"inner")
      .join(dfE,dfT("row_index") === dfE("row_index"),"inner")
      .drop("row_index")
    

    // this also works but looks bad:
    // dftrve.map(r => r.getString(0)+" " + r.getString(1)+" " + r.getString(2) +" "+ r.getString(3)).collect
    var list = dfT.map(_.toSeq.mkString(" ")).collect()
    return list(0)
  }
}
