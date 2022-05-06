$(document).ready(function () {
	//側邊欄下拉
	$(".menu>.drop--menu>a").click(function (e) {
		e.preventDefault();
		$(this).parent().toggleClass("active");
		$(this).parent().siblings().find('ul').slideUp();
		$(this).parent().find("ul").slideToggle();
	});


	//字體放大縮小
	$('.font-s').click(function (e) {
		$('.news-content .article p').css('font-size', '14px');
	});

	$('.font-m').click(function (e) {
		$('.news-content .article p').css('font-size', '18px');
	});

	$('.font-b').click(function (e) {
		$('.news-content .article p').css('font-size', '20px');
	});

	$('.font-s').click(function (e) {
		$('.class__content .article p').css('font-size', '14px');
	});

	$('.font-m').click(function (e) {
		$('.class__content .article p').css('font-size', '18px');
	});

	$('.font-b').click(function (e) {
		$('.class__content .article p').css('font-size', '20px');
	});
});

$(function () {
	$(".drop--menu>li>a").click(function (e) {
		e.preventDefault();
		$(this).toggleClass("active");
		$(this).parent().find('.menu--drop').slideToggle();
		$(this).parent().siblings().find('.menu--drop').slideUp();
	});

	//模擬交易所下拉選單切換內容
	$("#tradegroupChoice").on("change", function () {
		console.log($(this).val());
		switch ($(this).val()) {
			case "1": // 介面1
				$(".trade_set_content .a1").addClass('active');
				$(".trade_set_content .a2").removeClass('active');

				break;
			case "2": // 介面2
				$(".trade_set_content  .a2").addClass('active');
				$(".trade_set_content  .a1").removeClass('active');
				break;
			default:
				$(".trade_set_content  .a1").removeClass('active');
				$(".trade_set_content  .a2").removeClass('active');
				break;
		}
	});


});

function copyFn() {
	var val = document.getElementById('copyMy');
	window.getSelection().selectAllChildren(val);
	document.execCommand("Copy");
	alert("已成功複製！");
}
function setgroup() {
	$(this).click(function (e) {
		document.getElementById('setgroup').disabled = false;
		document.getElementById('setgroup2').disabled = true;
		document.getElementById('setgroup3').disabled = true;
		document.getElementById('setgroup4').disabled = true;
		document.getElementById('stoploss').disabled = true;
		document.getElementById('stoplossgroup').disabled = true;
		document.getElementById('stopcost').disabled = true;
		document.getElementById('stopcostgroup').disabled = true;
		document.getElementById('bullbearchoice').disabled = true;
		document.getElementById('bullbearchoice2').disabled = true;

	});

}
function setgroup2() {
	$(this).click(function (e) {
		document.getElementById('setgroup2').disabled = false;
		document.getElementById('setgroup3').disabled = false;
		document.getElementById('setgroup4').disabled = false;
		document.getElementById('bullbearchoice').disabled = false;
		document.getElementById('bullbearchoice2').disabled = false;
		document.getElementById('stoploss').disabled = false;
		document.getElementById('stoplossgroup').disabled = false;
		document.getElementById('stopcost').disabled = false;
		document.getElementById('stopcostgroup').disabled = false;
		document.getElementById('setgroup').disabled = true;
	});

}