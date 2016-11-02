//导入工具包 require('node_modules里对应模块')
var gulp = require('gulp'), //本地安装gulp所用到的地方
concat = require('gulp-concat'),
uglify = require('gulp-uglify'),
less = require('gulp-less');



gulp.task('testLess', function () {
    //编译src目录下的所有less文件
    //除了reset.less和test.less（**匹配src/less的0个或多个子文件夹）
    gulp.src(['src/less/*.less'])
        .pipe(less())
        .pipe(gulp.dest('static/css'));
});

////压缩css
//gulp.task('minifycss'，function () {
//    return gulp.src('src/css/*.css') //需要操作的文件
//        .pipe(rename({
//            suffix: '.min'
//        })) //rename压缩后的文件名
//        .pipe(minifycss()) //执行压缩
//        .pipe(gulp.dest('Css')); //输出文件夹
//});

gulp.task('scripts', function() {
  gulp.src(['src/js/count.js', 'src/js/layer.js', 'src/js/home.js', 'src/js/jweixin-1.0.0.js'])
    .pipe(concat('main.js'))
    .pipe(gulp.dest('static/js'))
});

gulp.task('img', function() {
  gulp.src(['src/img/**/*.png'])
    .pipe(gulp.dest('static/img'))
});

gulp.task('concatcss', function() {                                //- 创建一个名为 concat 的 task
    gulp.src(['src/css/*.css'])    //- 需要处理的css文件，放到一个字符串数组里
        .pipe(concat('style.css'))                            //- 合并后的文件名
        .pipe(gulp.dest('static/css'))                               //- 输出文件本地
});

gulp.task('testWatch', function () {
    gulp.watch('src/less/*.less', ['testLess']); //当所有less文件发生改变时，调用testLess任务
    gulp.watch('src/js/*.js', ['scripts']);
    gulp.watch('src/img/**/*.png', ['img']);
});

gulp.task('default', ['testLess','scripts','img', 'testWatch']); //定义默认任务 elseTask为其他任务，该示例没有定义elseTask任务

//gulp.task(name[, deps], fn) 定义任务  name：任务名称 deps：依赖任务名称 fn：回调函数
//gulp.src(globs[, options]) 执行任务处理的文件  globs：处理的文件路径(字符串或者字符串数组)
//gulp.dest(path[, options]) 处理完后文件生成路径