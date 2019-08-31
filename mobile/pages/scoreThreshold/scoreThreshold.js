// pages/scoreThreshold/scoreThreshold.js
var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    prevImg:'',
    score:10,
    loading:true
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    let that = this
    wx.request({
      url: app.globalData.host + '/getConfig',
      success(res){
        console.log(res.data)
        let score = res.data[0].fields.cvalue
        that.setData({score:parseFloat(score) * 1000})
        that.setData({ prevImg: app.globalData.host + '/setScoreThreshold?score=' + score })
      }
    })
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  //slider改变事件
  setThreshold: function(e){
    let score = e.detail.value
    let url = app.globalData.host + '/setScoreThreshold?score=' + (score / 1000)
    this.setData({score:score})
    this.setData({prevImg:url})
  },
  //恢复默认值
  recover: function(){
    let that = this
    wx.showModal({
      title: '提示',
      content: '您确认将检测为人头的阈值恢复为默认值吗？',
      success(res){
        if(res.confirm){
          let score = 10
          let url = app.globalData.host + '/setScoreThreshold?score=' + (score / 1000)
          that.setData({ score: score })
          that.setData({ prevImg: url })
        }
      }
    })
  },
  changeImg:function(){
    let that = this
    wx.chooseImage({
      count:1,
      success: function(res) {
        console.log(res)
        let impath = res.tempFilePaths[0]
        wx.uploadFile({
          url: app.globalData.host + '/changeTestImage',
          filePath: impath,
          name: 'img',
          success(res){
            console.log(res)
            let score = that.data.score + 1
            let url = app.globalData.host + '/setScoreThreshold?score=' + (score / 1000)
            that.setData({ prevImg: url })
            // score -= 1
            // url = app.globalData.host + '/setScoreThreshold?score=' + (score / 1000)
            // that.setData({ prevImg: url })
          }
        })
      },
    })
  }
})