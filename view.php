<?php

// over here i want to choose my dir

echo '<p></p><a href="index.html">Go back to Main Page</a><p></p>';

echo '<div class="checkbox-container">';
// this lists all files and i can tick and submit them
if (!isset($_POST['submit'])) { 

//$dir = '/var/www/html/Andrej/';
$dir = $_POST['dir'];
if(!isset($dir))
    $dir = 'Daten/';

 if ($dp = opendir($dir)) { 
 $files = array(); 
 $subdirs = array(); 
 while (($file = readdir($dp)) !== false) { 
  if (!is_dir($dir . $file)) { 
    $files[] = $file; 
  } else {
    $subdirs[] = $file;
  }
 } 
 closedir($dp); 
 } else { 
 exit('Directory not opened.'); 
 } 
 if($subdirs){
     echo '<form action="' . $_SERVER['PHP_SELF'] . '" method="post">'; 
     foreach ($subdirs as $d) {
        if($d == ".." || $d == "."){
            continue;
        }
      echo '<button type="submit" name="dir" value="' . $dir . $d . '/" />' . $d . '</button>' . '<p></p>'; 

     } 
 echo '</form>';  
 }
 if ($files) { 
 echo '<form action="' . $_SERVER['PHP_SELF'] . '" method="post">'; 
 foreach ($files as $file) { 
 
 
  //echo '<input type="checkbox" name="files[]" value="' . $file . '" />' . '&#8195;&#8195;<br />'; 
   
   echo '<input name="files[]" value="' . $dir . $file . '" class="inp-cbx" id="' . $file . '" type="checkbox"/>
          <label class="cbx" for="' . $file . '"><span>
            <svg width="12px" height="10px">
            <use xlink:href="#check"></use>
            </svg></span><span>' . $file . '</span></label><svg class="inline-svg">
            <symbol id="check" viewbox="0 0 12 10">
            <polyline points="1.5 6 4.5 9 10.5 1"></polyline>
            </symbol>
            </svg> <p></p>';
 
 } 
 echo '<p></<p><input type="submit" name="submit" value="submit" />' . 
  '</form>'; 
 } else { 
 //exit('No files found.'); 
 } 
} else { 
 if (isset($_POST['files'])) { 
 foreach ($_POST['files'] as $value) {
    
    //writing file contents into a variable
    $myfile = fopen($value, "r") or die("Unable to open file!");
    while(!feof($myfile)) {
      $csv_data .= fgets($myfile);  
    }
    fclose($myfile);  
 } 
 } else { 
 exit('No files selected'); 
 }

echo '</div>';

}
?>

<!DOCTYPE html> <!-- Write your comments here -->
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Graph</title>
   <link rel="stylesheet" href="./large2.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prefixfree/1.0.7/prefixfree.min.js"></script>
  
<!--    <meta charset="UTF-8"> -->
    
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

   
    <script src="highcharts.js"></script>
    <script src="data.js"></script>
    <script src="exporting.js"></script>
    <script src="export-data.js"></script>
    <script src="accessibility.js"></script>
    <script src="jquery-3.5.1.min.js"></script>
    <script src="papaparse.js"></script>
    
   <!-- 
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://code.highcharts.com/highcharts.js"></script> 
    <script src="https://code.highcharts.com/modules/data.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    <script src="https://code.highcharts.com/highcharts-more.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/4.1.2/papaparse.js"></script>
    <title>Airmeter</title>
 -->


</head>

<body>

    <div class="BackButton">    
        </div>

    <div id="container1"></div>
    <div id="container2"></div>

    <script type="text/javascript">

        function drawChart(raw_data) {

            let newTitle;
            
            console.log(raw_data);

            let chart = Highcharts.chart('container1', {

                chart: {
                    zoomType: 'xy',
                    events: {
                        load: function () {
                            this.update({
                                title: {
                                    text: 'AirMeter: ' + newTitle 
                                }
                            })
                        }

                    }

                },

                xAxis: {

                    title: {
                        text: 'Zeit'
                    }
                },

                yAxis: {


                    title: {
                        text: 'CO2 in ppm'
                    }

                },

                exporting: {
                    enabled: true
                },


                title: {
                    text: null
                },

                credits: {
                    enabled: false
                },

                data: {
                    csv: raw_data,
                    parsed(e) {
                        newTitle = e[0][5]  //set the first column as title of the chart
                        
                        e.shift()

                    },
                    complete: function(options){
                    options.series.splice(0,1)
                    options.series.splice(0,1)
                    options.series.splice(0,1)
                    options.series.splice(0,1)

                    }

                }


            });
            
        }


        drawChart('<?php echo json_encode($csv_data); ?>');


////////////////////////////////////////////////////////////////////////

function drawChart2(raw_data) {

let newTitle;

console.log(raw_data);

let chart = Highcharts.chart('container2', {

    chart: {
        zoomType: 'xy',
        events: {
            load: function () {
                this.update({
                    title: {
                        text: 'AirMeter: ' + newTitle 
                    }
                })
            }

        }

    },

    xAxis: {

        title: {
            text: 'Zeit'
        }
    },

    yAxis: {


        title: {
            text: 'Temperatur'
        }

    },

    exporting: {
        enabled: true
    },


    title: {
        text: null
    },

    credits: {
        enabled: false
    },

    data: {
        csv: raw_data,
        parsed(e) {
            newTitle = e[0][5]  //set the first column as title of the chart
            
            e.shift()

        },
        complete: function(options){
        options.series.pop()
        options.series.pop()
        options.series.pop()
        options.series.pop()
    
        

        }

    }


});

}


drawChart2('<?php echo json_encode($csv_data); ?>');

    </script>
    

</body>

</html>
