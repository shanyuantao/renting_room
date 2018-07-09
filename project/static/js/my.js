


$(document).ready(function () {

    $.get('/shan/area/', function (data) {
        if (data.code == 200) {
            var area_html_list = '';
            area_html_list = '<a href="#" class="inpro_cura">' + '不限' + '</a>';
            for (var i=0; i< data.area_list.length; i++){

                area_html_list += '<a href="/shan/area_query_house/' + data.area_list[i].id + '/" >' + data.area_list[i].name + '</a>'
            }

            $('#area_list').append(area_html_list);

        } else {
            alert('访问区域函数失败');
        }
    });


    var price_html_list = '';

    price_html_list = '<a href="#" class="inpro_cura">' + '不限' + '</a>';
    price_html_list += '<a href="/shan/price_query_house/0/500/">' + '500元以下' + '</a>';
    price_html_list += '<a href="/shan/price_query_house/500/1000/">' + '500-1000元' + '</a>';
    price_html_list += '<a href="/shan/price_query_house/1000/2000/">' + '1000-2000元' + '</a>';
    price_html_list += '<a href="/shan/price_query_house/2000/3000/">' + '2000-3000元' + '</a>';
    price_html_list += '<a href="/shan/price_query_house/3000/5000/">' + '3000-5000元' + '</a>';
    price_html_list += '<a href="/shan/price_query_house/5000/8000/">' + '5000-8000元' + '</a>';
    price_html_list += '<a href="/shan/price_query_house/8000/20000/">' + '8000元以上' + '</a>';


    $('#price_list').append(price_html_list);

    var acreage_html_list = '';
    acreage_html_list = '<a href="#" class="inpro_cura">' + '不限' + '</a>';
    acreage_html_list += '<a href="/shan/acreage_query_house/0/50/">' + '50平米以下' + '</a>';
    acreage_html_list += '<a href="/shan/acreage_query_house/50/70/">' + '50-70平米' + '</a>';
    acreage_html_list += '<a href="/shan/acreage_query_house/70/90/">' + '70-90平米' + '</a>';
    acreage_html_list += '<a href="/shan/acreage_query_house/90/110/">' + '90-110平米' + '</a>';
    acreage_html_list += '<a href="/shan/acreage_query_house/110/130/">' + '110-130平米' + '</a>';
    acreage_html_list += '<a href="/shan/acreage_query_house/130/150/">' + '130-150平米' + '</a>';
    acreage_html_list += '<a href="/shan/acreage_query_house/150/200/">' + '150-200平米' + '</a>';
    acreage_html_list += '<a href="/shan/acreage_query_house/200/500/">' + '200-500平米' + '</a>';

    $('#acreage_list').append(acreage_html_list);

    $.get('/shan/house_type/', function (data) {
        if (data.code == 200){
            alert('hahha');
            var type_html_list = '';
            type_html_list = '<a href="#" class="inpro_cura">' + '不限' + '</a>';
            for (var i=0; i<data.type_list.length; i++){
                type_html_list += '<a href="/shan/price_query_house/' + data.type_list[i].id + '/" >' + data.type_list[i].name + '</a>'
            }

            $('#type_list').append(type_html_list);


        }
    });





});
//
// <div class="prolist_one prolist_one_bl01 mt20">
//        <h2 class="prolist_one_tit"><span>抵押</span>汽车销售服务企业补充流动资金（三期）
//        </h2>
//        <ul class="prolist_one_ul clearfix">
//            <li>
//                年华收益：<strong>12.49%</strong><br>
//                还款方式：按月付息，到期还本
//            </li>
//            <li>
//                剩余期限：<i>308</i>天<br>
//                 保障机构：中融兴业融资担保有限公司
//            </li>
//            <li class="prolist_press">
//                募集金额：<strong>9,900.00</strong> 元 <br>
//                认购进度：<span class="ui-progressbar-mid ui-progressbar-mid-100">100%</span>
//            </li>
//            <li class="prolist_btn">
//                 <a href="/static/11112/detail.html" class="pro_btn">立即投资</a>
//            </li>
//        </ul>
//  </div>