/**
 * Created by tanglihao on 2015/12/31.
 * ajax-input.js 是一个基于jquery和ajax请求的输入框插件
 */

;(function ($, window, document, undefined) {

    // 构造方法ele指调用插件的元素，opts指传入的参数
    var AjaxInput = function (ele, opts) {
        this.$element = ele;
        this.defaults = {
            'ajaxUrl': '',             // 请求路径
            'requestMethod': 'get',    // 默认请求为get,（目前只支持get）
            'extraParams': {},         // 扩展ajax参数，默认没有更多的请求参数
            'showName': ''             // 要显示的json数组的键（也就是某一个字段名）
        };
        this.options = $.extend({}, this.defaults, opts);
    };

    // 定义方法
    AjaxInput.prototype = {
        ajaxRequest: function () {
            // 创建ul节点
            var $itemList = $('<ul></ul>').addClass("item-list");
            var ajaxUrl = this.options.ajaxUrl;
            var showName = this.options.showName;
            var $input = this.$element;
            var extraPara = this.options.extraParams;
            // 监听输入框的按键松开事件，实现当输入改变时
            this.$element.keyup(function (e) {
                if(e.keyCode != 38 && e.keyCode != 40 && e.keyCode != 13) {
                    // 获取输入框的内容作为关键字和ajax请求参数
                    var keyword = $(this).val();
                    extraPara["keyword"] = keyword;
                    // 发送ajax到后台请求数据
                    $.get(ajaxUrl, extraPara, function(data){
                        // 删除原来的ul节点
                        $itemList.find("li").remove();
                        $itemList.remove();
                        // 遍历后台返回的json数组，并生成li节点
                        for(var item in data) {
                            alert(data[item].fields[showName]);
                            // 创建li节点
                            var $item = $('<li></li>').addClass("li-item");
                            $item.text(data[item].fields[showName]);
                            $item.attr("num", "li-"+item.toString());
                            $itemList.append($item);
                        }
                        // 监听li的鼠标点击事件
                        if ($itemList.find('li').length > 0) {
                            $('.ajax-input').append($itemList);
                            $itemList.find('li').mousedown(function () {
                                // 设置输入框的文字
                                $input.val($(this).text());
                                $itemList.remove();
                            });
                        }else {
                            // 如果需要设计没有选项的样式，可以在这里添加控制样式的代码
                        }
                    });
                }
            }).keypress(function (e) {
                // 监听键盘的上下按键，实现上下选择选项的功能
                var liLen = $itemList.find('li').length;
                if(liLen > 0) {
                    //alert($itemList.find('li').hasClass("focus-li"));
                    if($itemList.find('li').hasClass("focus-li")) {
                        // 获取
                        var focusNum = $itemList.find('li.focus-li').attr("num").split("-")[1];
                        if(e.keyCode == 38) {
                            if(focusNum == 0) {
                                // 焦点在第一个li上
                                $itemList.find('li.focus-li').removeClass("focus-li");
                                $itemList.find('li').last().addClass("focus-li");
                            }else {
                                $itemList.find('li.focus-li').prev().addClass("focus-li");
                                $itemList.find('li.focus-li').next().removeClass("focus-li");
                            }
                        }else if(e.keyCode == 40) {
                            if (focusNum == liLen-1) {
                                // 焦点在最后一个li上
                                $itemList.find('li.focus-li').removeClass("focus-li");
                                $itemList.find('li').first().addClass("focus-li");
                            } else {
                                $itemList.find('li.focus-li').next().addClass("focus-li");
                                $itemList.find('li.focus-li').prev().removeClass("focus-li");
                            }
                        }else if(e.keyCode == 13) {
                            // 回车选中
                            var sel = $itemList.find('li.focus-li').text();
                            $input.val(sel).blur();
                        }
                    }
                    else{
                        // 没有li被选中
                        if (e.keyCode == 38) {
                            // 上按键
                            $itemList.find('li:last-child').addClass("focus-li");
                        } else if (e.keyCode == 40) {
                            // 下按键
                            $itemList.find('li:first-child').addClass("focus-li");
                        }
                    }
                }
            }).blur(function () {
                // 删除输入框的焦点
                //$itemList.remove();
            });
            return this;
        }
    };

    // 使用对象
    $.fn.ajaxInput = function (options) {
        var objectInput = new AjaxInput(this, options);
        return objectInput.ajaxRequest();
    };
})(jQuery, window, document);