import * as echarts from '../../ec-canvas/echarts';

const app = getApp();

function initChart(canvas, width, height) {
  const chart = echarts.init(canvas, null, {
    width: width,
    height: height
  });
  canvas.setChart(chart);

  var option = {
    title: {
      text: '人流量'
    },
    animation: false,
    legend: {
      data: ['基教前', '校门口']
    },
    xAxis: {
      name: '时间 / s',
      data: []
    },
    color: ['#ff7f50', '#87cefa'],
    yAxis: {},
    series: [{
      name: '基教前',
      type: 'line',
      data: [],
      markLine: {
        symbol: 'none',
        data: [
          { name: '警戒线', yAxis: 50 },
        ]
      }
    }, {
      name: '校门口',
      type: 'line',
      data: [39, 52, 40, 11, 6, 50, 10, 47, 9, 32, 35, 45, 43, 29, 33, 37, 14, 22, 40, 50, 39, 18, 56, 7, 4, 4, 17, 32, 33, 36, 51, 38, 9, 57, 13, 25, 36, 23, 23, 8, 28, 41, 35, 28, 13, 33, 39, 53, 3, 5, 26, 14, 28, 47, 54, 34, 9, 24, 27, 52]
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
      onInit: initChart
    }
  },

  onReady() {
  }
});
