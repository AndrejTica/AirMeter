//document.addEventListener('DOMContentLoaded', () =>{    //callback function
  
    var d = new Date();
    var t = d.getDate(); //get tag
    var m = d.getMonth() + 1; //get monat, plus one cuz january is 0
    var j = d.getFullYear();
    var tagString = t.toString();   //we need to convert the numbers to strings
    var monatString = m.toString();
    var jahrString = j.toString();


    var options = {
        chart:{

            zoomType: 'xy'

        },

        // tooltip:{
        //     formatter(){
        //         return `Zeit - ${this.x}. ppm - ${this.y}`;

        //     }

        // },

        exporting:{
            enabled: true
        },

        credits:{                   //credit aus
            enabled: false
        },

        title: {
            text: 'Airmeter: ' + tagString +'.'+ monatString + '.' + jahrString //just d for full time
        },

        xAxis:{
            type: 'Uhrszeit', //funktioniert nur wenn ich monat und tag auch hab
            title:{
                text: 'Zeit'
            }
        },

        yAxis:{
          

            title:{
                text: 'CO2 in ppm'
            }

        } 
    };
       
       
     $.get('test.csv', csv => {
        options.data = {
            csv
        };
        Highcharts.chart('container', options); //highchart global variable from library 
     });


     function parseCSVData(csvFile){
        //empty array for storing our data
        var data = [];
        //split into lines
        var lines = csvFile.split("\n");
        //go through each line
        $.each(lines, function (lineNumber, line){
            if (lineNumber != 0){
                var fields = line.split(",");
                if (fields.lenght == 7){
                    var timestamp = Date.parse(fields[0]);
                    var value = parseFloat(fields[6]);
                    data.push([timestamp, value]);
                }
            }

        });
     }

  
















    // options.data = {
    //     csvURL: '/home/andrej/Documents/LastSchoolYear/Airmeter/website/test.csv',
    //     enablePolling: true,
    //     dataRefreshRate: 2
    // }
    // Highcharts.chart('container', options);
//});






/*

*/
