import React from 'react';

const demo = () => {
  return (
    <div>
      <Container>
        <Row>
          {blog.map((blog) => {
            <ProductItems blog={blog} />;
          })}
          <ProductItems />
        </Row>
      </Container>
    </div>
  );
};

export default demo;
