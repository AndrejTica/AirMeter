<?php
// over here i want to choose my dir


// php code can not be viewed on website so you use echo
// php can print html syntax into "file" via echo
echo '<p></p><a href="index.html">Go back to Main Page</a><p></p>';

echo '<div class="checkbox-container">';


//isset(<request>) checks if value in request is set

// this lists all files and i can tick and submit them
if (!isset($_POST['submit']))
//checks if input type "submit" is set (Button on website pressed) 
//if it is not set, then ifcase is true and you can navigate further
{
    $dir = $_POST['dir'];
    //value 'dir' in post-request is the new dir
    //value dir is the folder that you select
    
    if (!isset($dir)) $dir = 'Daten/';
    //first time executeing the page 'dir' in post-request is not set,
    //so it's set now to the folder that includes .csv files

    if ($dp = opendir($dir))//opens directory as a directory file
    {
        $files = array(); //declaired array
        $subdirs = array(); //declaired array
        while (($content = readdir($dp)) !== false) //reads directory contents one by one -> while and stores them in $content
        {
            if (!is_dir($dir . $content)) //stores files in files and dirs in dirs
            {
                $files[] = $content;
            }
            else
            {
                $subdirs[] = $content;
            }
        }
        closedir($dp); //closing directory
    }
    else
    {
        exit('Directory not opened.'); // error handling
    }
    if ($subdirs) //if there are subdirs they are listed as buttons
    {
        echo '<form action="' . $_SERVER['PHP_SELF'] . '" method="post">'; //only with <form> tag you can execute get- or post-requests with you need for the buttons
        foreach ($subdirs as $d)
        {
            if ($d == ".." || $d == ".") //on linux there are ".." and "." dirs, which point onto the parent directory and the current directory, which we do not want the user to see
            {
                continue;
            }
            echo '<button type="submit" name="dir" value="' . $dir . $d . '/" />' . $d . '</button>' . '<p></p>';
            //$d is name of directory an is shown on button 
            //value of button is the 'dir' (name="dir") in post-request an needs to be set for next iterations

        }
        echo '</form>';
    }
    if ($files) //if there are files they are listed as checkboxes
    {
        echo '<form action="' . $_SERVER['PHP_SELF'] . '" method="post">'; //only with <form> tag you can execute get- or post-requests with you need for the buttons
        foreach ($files as $file)
        {

            echo '
                <input name="files[]" value="' . $dir . $file . '" class="inp-cbx" id="' . $file . '" type="checkbox"/>
                <label class="cbx" for="' . $file . '">
                    <span>
                        <svg width="12px" height="10px">
                            <use xlink:href="#check"></use>
                        </svg>
                    </span>
                    <span>
                        ' . $file . '
                    </span>
                </label>
                <svg class="inline-svg">
                    <symbol id="check" viewbox="0 0 12 10">
                        <polyline points="1.5 6 4.5 9 10.5 1"></polyline>
                    </symbol>
                </svg> <p></p>
            ';
        }
        echo '<p></<p><input type="submit" name="submit" value="submit" />' . '</form>';
        //variable files[] in post-request is set with the files of all ticked checkboxes
    }
}
else
{
    if (isset($_POST['files'])) // if files in post-requests is set
    {
        foreach ($_POST['files'] as $value) // loop through all files
        {

            //writing file contents into a variable
            $myfile = fopen($value, "r") or die("Unable to open file!"); //if you can not open, den write "Unable to open file!"
            while (!feof($myfile)) //go through file-contents char by char until char is end of file char
            {
                $csv_data .= fgets($myfile); // write into csv_data which will be used for drawgraph() function
            }
            fclose($myfile); //close file
        }
    }
    else
    {
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

