var app1 = new Vue({
el: '#word',
data:{
    message:'',
    answer:'',
},
methods:{
    check:function(){
        if(this.answer.replace(/^\s+|\s+$/g, '')=='{{word.english}}'){
            this.message='<p style="color:green;margin:0px,0px,0px,50px;">You are right</p>';
        }else{
            this.message='<p style="color:red;margin:0px,0px,0px,50px;">You are wrong</p>';
        }
    },
    hint:function(){
    this.message='<p style="color:pink;margin:0px,0px,0px,50px;">{{word.english}}</p>';
        },
    clear:function(){
        this.answer='';
        this.message='';
    }
}
})