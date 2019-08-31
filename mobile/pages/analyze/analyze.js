// pages/analyze/analyze.js
import * as echarts from '../../ec-canvas/echarts';
//获取应用实例
const app = getApp();

function initChart(canvas, width, height) {
  const chart = echarts.init(canvas, null, {
    width: width,
    height: height
  });
  canvas.setChart(chart);

  var option = {
    title: {
      text: '最大人流'
    },
    animation: false,
    legend: {
      data: ['基教前', '校门口']
    },
    xAxis: {
      name: 't/s',
      data: []
    },
    color: ['#ff7f50', '#87cefa'],
    yAxis: {},
    series: [{
      name: '基教前',
      type: 'line',
      data: [0, 0, 1, 1, 3, 3, 10, 11, 8, 6, 7, 4, 9, 5, 4, 1, 2, 1, 1, 2, 3, 6, 6, 4, 8, 15, 16, 12, 9, 5, 0, 0, 1, 1, 3, 3, 10, 11, 8, 6, 7, 4, 9, 5, 4, 1, 2, 1, 1, 2, 3, 6, 6, 4, 8, 15, 16, 12, 9, 5],
      markLine: {
        symbol: 'none',
        data: [
          { name: '警戒线', yAxis: 50 },
        ]
      }
    }, {
      name: '校门口',
      type: 'line',
        data: [6, 5, 5, 9, 12, 16, 15, 8, 4, 6, 6, 3, 2, 1, 1, 2, 1, 4, 5, 9, 4, 7, 6, 8, 11, 10, 3, 3, 1, 1, 0, 0, 5, 9, 12, 16, 15, 8, 4, 6, 6, 3, 2, 1, 1, 2, 1, 4, 5, 7, 6, 8, 11, 10, 3, 3, 1, 1]
    }],

  };

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
      onInit: initChart,
    },
    dateOpt:7
  },

  onReady() {
  },
  
  changeDateOpt(e){
    let d = e.currentTarget.dataset.d
    this.setData({dateOpt:d})
  }
});
