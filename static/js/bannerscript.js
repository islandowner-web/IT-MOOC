var timer = null,
    index = 0,
    pics = byId("banner").getElementsByTagName("div"),
    dots = byId("dots").getElementsByTagName("span"),
    size = pics.length,
    prev = byId("prev"),
    next = byId("next"),
    menuItems = byId("menu-content").getElementsByTagName("div"),
    subMenu = byId("sub-menu"),
    subItems = subMenu.getElementsByClassName("inner-box");

function addHandler(element, type, handler) {
    if (element.addEventListener) {
        element.addEventListener(type, handler, true);
    }
    else if (element.attachEvent) {
        element.attachEvent('on' + type, handler);
    }
    else {
        element['on' + type] = handler;
    }
}

function byId(id){
	return typeof(id)==="string"?document.getElementById(id):id;
}

// 清除定时器,停止自动播放
function stopAutoPlay(){
	if(timer){
       clearInterval(timer);
	}
}

// 图片自动轮播
function startAutoPlay(){
   timer = setInterval(function(){
       index++;
       if(index >= size){
          index = 0;
       }
       changeImg();
   },3000)
}

function changeImg(){
   for(var i=0,len=dots.length;i<len;i++){
       dots[i].className = "";
       pics[i].style.display = "none";
   }
   dots[index].className = "active";
   pics[index].style.display = "block";
}

function slideImg(){
    startAutoPlay();
    var main = byId("main");
    var banner = byId("banner");
    var menuContent = byId("menu-content");

    addHandler(main,"mouseover",stopAutoPlay);
    addHandler(main,"mouseout",startAutoPlay);

    // 点击导航切换
    for(var i=0,len=dots.length;i<len;i++){
       dots[i].id = i;
       addHandler(dots[i],"click",function(){
           index = this.id;
           changeImg();
       })
    }

    // 下一张
    addHandler(next,"click",function(){
       index++;
       if(index>=size) index=0;
       changeImg();
    })

    // 上一张
    addHandler(prev,"click",function(){
       index--;
       if(index<0) index=size-1;
       changeImg();
    })

    // 菜单
    for(var m=0,mlen=menuItems.length;m<mlen;m++){
        menuItems[m].setAttribute("data-index",m);
        addHandler(menuItems[m],"mouseover",function(){
            subMenu.className = "sub-menu";
            var idx = this.getAttribute("data-index");
            for(var j=0,jlen=subItems.length;j<jlen;j++){
               subItems[j].style.display = 'none';
               menuItems[j].style.background = "none";
            }
            subItems[idx].style.display = "block";
            menuItems[idx].style.background = "rgba(0,0,0,0.1)";
        });
    }

    addHandler(subMenu,"mouseover",function(){
        this.className = "sub-menu";
    });

    addHandler(subMenu,"mouseout",function(){
        this.className = "sub-menu hide";
    });

    addHandler(banner,"mouseout",function(){
        subMenu.className = "sub-menu hide";
    });

    addHandler(menuContent,"mouseout",function(){
        subMenu.className = "sub-menu hide";
    });
}

addHandler(window,"load",slideImg);