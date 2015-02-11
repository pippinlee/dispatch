var Timer = React.createClass({
    getInitialState: function() {
        return {secondsElapsed: 0};
    },
    tick: function() {
        this.setState({secondsElapsed: this.state.secondsElapsed + 1});
    },
    componentDidMount: function() {
        this.interval = setInterval(this.tick, 1000);
    },
    componentWillUnmount: function() {
        clearInterval(this.interval);
    },
    render: function() {
        return (
          <div>Seconds Elapsed: {this.state.secondsElapsed}</div>
        );
    }
});


var Gallery = React.createClass({
    getInitialState: function(){
        return {
            images: {},
            images_list: [],
            current_image: false,
            image: false,
            image_height: false,
        }
    },
    componentWillMount: function() {
        dispatch.articleAttachments(this.props.article, function(data){
            var images = {};
            $.each(data.results, function(key, image){
                images[image.id] = key;
            });

            this.setState({
                'images': images,
                images_list: data.results,
                image_height: $(window).height() - 200,
            });

            this.setupEventListeners();
            this.displayCurrentImage();

        }.bind(this));
    },
    setupEventListeners: function(){
        key('left', this.previous);
        key('right', this.next);
        key('esc', this.close);

        $(this.getDOMNode()).mouseup(function (e)
        {
            var container = $(this.getDOMNode()).find(".image-container");
            if (!container.is(e.target) && container.has(e.target).length === 0)
            {
                this.close();
                $('body').removeClass('no-scroll');
            }
        }.bind(this));
    },
    setCurrentImage: function(image_id){
        this.setState({
            current_image: image_id,
        });
    },
    displayCurrentImage: function(){
        var attachment = this.state.images_list[this.state.images[this.state.current_image]];
        this.setState({
            image: attachment.image.url,
            caption: attachment.caption,
        });
    },
    open: function(image_id){
        this.setCurrentImage(image_id);
        if(this.state.images_list.length != 0){
            this.displayCurrentImage();
        }
        this.setState({
            visible: true,
        });
    },
    close: function(){
        this.setState({
            visible: false,
        });
    },
    previous: function(){
        if(this.state.images[this.state.current_image] == 0) return;
        this.setCurrentImage(this.state.current_image - 1);
        this.displayCurrentImage();
    },
    next: function(){
        if(this.state.images[this.state.current_image] == this.state.images_list.length - 1) return;
        this.setCurrentImage(this.state.current_image + 1);
        this.displayCurrentImage();
    },
    renderImage: function(){
        if(this.state.image){
            var imageStyle = {
                maxHeight: this.state.image_height,
            };
            return (
                <div className="slide">
                    <img className="slide-image" style={imageStyle} src={'http://dispatch.dev:8888/media/' + this.state.image } />
                    <p className="slide-caption">{this.state.caption}</p>
                    <div className="navigation">
                        <a className="prev-slide" href="#"><i className="fa fa-chevron-left"></i></a>
                        <span className="curr-slide"></span> &nbsp; of &nbsp; <span className="total-slide"></span>
                        <a className="next-slide" href="#"><i className="fa fa-chevron-right"></i></a>
                    </div>
                </div>
            );
        }
    },
    render: function() {
        if(this.state.visible){
            var visible = "visible";
        } else {
            var visible = "";
        }
        return (
            <div className={'slideshow ' + visible}>
                <div className="image-container">
                    <div className="image-inner">
                    {this.renderImage()}
                    </div>
                </div>
            </div>
        );
    }
});

var article = $('article').data("id");
var gallery = React.createElement(Gallery, { 'article': article });
$('.article-attachment').click(function(){

    if(!gallery.isMounted){
        gallery = React.render(
            gallery,
            document.getElementById('gallery')
        );
    }

    if(gallery.state.visible){
        gallery.close();
    } else {
        var image_id = $(this).data("id");
        gallery.open(image_id);
    }

});