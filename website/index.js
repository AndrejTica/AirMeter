$.ajax({
  type: "GET",
  url: "test.csv",
  success: function (data) {
    setTitle(data)
  }
});


function setTitle(raw_data){

  let newTitle;
 
  
  let chart = Highcharts.chart('container', {
    
    chart: {
      zoomType: 'xy',
      events: {
        load: function() {
          this.update({
            title: {
              text: 'Airmeter: '+ newTitle
            }
          })
        }
        
      }
    
    },
    
    xAxis:{
     
      title:{
          text: 'Zeit'
      }
  },

  yAxis:{
      

    title:{
        text: 'CO2 in ppm'
    }

} ,
  
exporting:{
  enabled: true
},


    title: {
      text: null
    },

    credits:{                   //credit aus
      enabled: false
  },

    data: {
      csv: raw_data,
      parsed(e) {
        newTitle=e[0][1]
        e.shift()
        
      }
      
    }
  
  
  });

}

