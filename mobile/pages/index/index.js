//index.js
import * as echarts from '../../ec-canvas/echarts';
//获取应用实例
const app = getApp();

//图表配置
var option = {
  title: {
    text: ''
  },
  animation: false,
  legend: {
    data: []
  },
  xAxis: {
    name: 't/s',
    data: []
  },
  color: ['#ff7f50', '#87cefa'],
  yAxis: {},
  series: [],
  tooltip:{
    show:true,
    trigger:'axis'
  },
  //自定义图标事件
  toolbox: {
    feature: {
      myTool1: {
        show: true,
        title: '自定义扩展方法',
        icon: '/images/alarm.png',
        onclick: function () {
          alert('myToolHandler2')
        }
      }
    }
  }

};

//初始化图表
function initChart(canvas, width, height) {
  const chart = echarts.init(canvas, null, {
    width: width,
    height: height
  });
  canvas.setChart(chart);
  chart.setOption(option);
  return chart;
}

Page({
  onShareAppMessage: function (res) {
    return {
      title: 'ECharts 可以在微信小程序中使用啦！',
      path: '/pages/index/index',
      success: function () { },
      fail: function () { }
    }
  },
  data: {
    ec: {
      onInit: initChart
    },
    alarmThreshold:50
  },

  onReady() {
    let that = this
    this.oneComponent = this.selectComponent('#mychart-dom-line')

    //监测未读消息
    if(!this.data.alarmTimer){
      var alarmTimer = setInterval(function () {
        wx.request({
          url: app.globalData.host + '/peoplecount/unreadAlarm',
          success(res) {
            console.log(res)
            that.setData({unread:res.data.alarmNum})
          }
        })
      }, 1000)
      that.setData({alarmTimer:alarmTimer})
    }

    wx.request({
      url: app.globalData.host + '/getSites',
      success(res){
        console.log(res)
        //初始化每个地点数据()
        for (var i = 0; i < res.data.length; i++)
          that.initChart(res.data[i])

        //每个地点数据实时变化
        var timer = setInterval(function () {
          for (var i = 0; i < res.length; i++) {
            that.scrollData(res.data[i].pk)
          }
        }, 500)
      }
    })
  },

  //初始化第n个地点数据
  initChart(site){
    let that = this
    wx.request({
      url: app.globalData.host + '/peoplecount/selectNewest?limit=60&site=' + site.pk,
      success(res) {
        console.log(res.data)
        var x = res.data.map(function (d) { return parseInt(d.fields.rtime.slice(17, 19)) })
        var y = res.data.map(function (d) { return d.fields.rnum })

        var serie = {
          name: site.fields.sname,
          type: 'line',
          data: y,
          markLine: {
            symbol: 'none',
            data: [
              { name: '警戒线', yAxis: site.fields.salarm },
            ]
          }
        }
        option.legend.data.push(site.fields.sname)
        option.series.push(serie)
        option.xAxis.data = x
        console.log(option)
        that.updateChart()
      }
    })
  },

  scrollData(n){
    let that = this
    wx.request({
      url: app.globalData.host + '/peoplecount/selectNewest?limit=1&site=' + n,
      success(res) {
        // console.log(res.data)
        var x = parseInt(res.data[0].fields.rtime.slice(17, 19))
        // 人数大于警戒值
        if(x >= that.alarmThreshold)
        {
          wx.showModal({
            title: '12:20',
            content: '地点人数达到阈值以上',
          })
        }
        if (x != option.series[n - 1].data[option.series[n - 1].data.length - 1])
        {
          option.series[n - 1].data.shift()
          option.series[n - 1].data.push(x)
          that.updateChart()
        }
      }
    })
  },

  //更新图表
  updateChart(){
    let that = this
    this.oneComponent.init((canvas, width, height) => {
      const chart = echarts.init(canvas, null, {
        width: width,
        height: height
      });
      chart.setOption(option)
      // that.chart = chart;
      return chart;
    });
  },

  alarm(e){
    wx.navigateTo({
      url: '/pages/alarm/alarm',
    })
  }
});
