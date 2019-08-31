// pages/feedback/feedback.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
  
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
  feedback:function(e){
    console.log(e)
    if(e.detail.value.content == ''){
      wx.showToast({
        title: '请输入内容',
        icon:'none'
      })
      return
    }
    wx.request({
      url: app.globalData.host + 'AddFeedback?',
      data:e.detail.value,
      success(res){
        if(res.statusCode == 200){
          if(res.data.status == 'OK'){
            wx.showToast({
              title: '感谢您的宝贵意见！',
              success(res){
                setTimeout(function(){
                  wx.navigateBack({})
                },1500)
              }
            })
          }else{
            wx.showModal({
              title: '提示',
              content: '提交失败',
              showCancel:false
            })
          }
        }else{
          wx.showToast({
            title: '网络错误',
            image:'/image/close.png'
          })
        }
      }
    })
  }
})