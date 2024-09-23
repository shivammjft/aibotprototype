import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const ImageSlider = () => {
  const settings = {
    dots: true, // Enable dots at the bottom for navigation
    infinite: true, // Infinite scrolling
    speed: 500, // Transition speed
    slidesToShow: 4, // Show four slides at a time
    slidesToScroll: 1, // Scroll one slide at a time
    nextArrow: <NextArrow />,
    prevArrow: <PrevArrow />,
  };

  return (
    <div className="w-full  h-[8rem] mt-[2rem]  p-2 ">
      <Slider {...settings}>
        <div>
          <img
            src="https://www.jellyfishtechnologies.com/wp-content/uploads/2023/10/jBilling.png"
            alt="Slide 1"
            className="w-[10rem] h-[8rem] rounded-md ml-[7rem] "
          />
        </div>
        <div>
          <img
            src="https://www.jellyfishtechnologies.com/wp-content/uploads/2023/10/payleadr.svg"
            alt="Slide 2"
            className="w-[10rem] h-[8rem] rounded-md ml-[7rem] "
          />
        </div>
        <div>
          <img
            src="https://www.jellyfishtechnologies.com/wp-content/uploads/2023/10/patra_logo_black.png"
            alt="Slide 3"
            className="w-[10rem] h-[8rem] rounded-md ml-[7rem] "
          />
        </div>
        <div>
          <img
            src="https://www.jellyfishtechnologies.com/wp-content/uploads/2023/10/certvault.svg"
            alt="Slide 4"
            className="w-[10rem] h-[8rem] rounded-md ml-[7rem]"
          />
        </div>
        <div>
          <img
            src="https://www.jellyfishtechnologies.com/wp-content/uploads/2023/10/heffins.png"
            alt="Slide 5"
            className="w-[10rem] h-[8rem] rounded-md ml-[7rem] "
          />
        </div>
        <div>
          <img
            src="https://www.jellyfishtechnologies.com/wp-content/uploads/2023/10/Revierjagd-Luzern-300x113.png"
            alt="Slide 6"
            className="w-[10rem] h-[8rem] rounded-md ml-[7rem] "
          />
        </div>
        <div>
          <img
            src="https://www.jellyfishtechnologies.com/wp-content/uploads/2023/11/kfm.webp"
            alt="Slide 7"
            className="w-[10rem] h-[8rem] rounded-md ml-[7rem] "
          />
        </div>
        <div>
          <img
            src="https://www.jellyfishtechnologies.com/wp-content/uploads/2023/11/fm.webp"
            alt="Slide 8"
            className="w-[10rem] h-[8rem] rounded-md ml-[7rem] "
          />
        </div>
      </Slider>
    </div>
  );
};

const NextArrow = (props) => {
  const { onClick } = props;
  return (
    <div
      className="absolute top-1/2 right-2 transform -translate-y-1/2 text-[#2B9AC1] p-2 rounded-full cursor-pointer"
      onClick={onClick}
    >
      &#10095;
    </div>
  );
};

const PrevArrow = (props) => {
  const { onClick } = props;
  return (
    <div
      className="absolute top-1/2 left-2 transform -translate-y-1/2  text-[#2B9AC1] p-2 rounded-full cursor-pointer z-10 "
      onClick={onClick}
      style={{ zIndex: 10 }}
    >
      &#10094;
    </div>
  );
};

export default ImageSlider;
