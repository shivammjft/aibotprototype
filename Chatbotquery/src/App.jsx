import { useState } from "react";
import "./App.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to the Rajnigandha Chatbot Demo</h1>
        <p>This is a chatbot demo for Rajnigandha.</p>
      </header>

      <span className="info-data-section">
        <h2>About Rajnigandha</h2>
        <h5>
          Founded in 1983 by the DS Group, Rajnigandha Pan Masala is a premium
          brand that has redefined the traditional experience of paan. Rooted in
          the age-old Indian custom of offering paan as a gesture of
          hospitality, Rajnigandha presents a modern, dry alternative to the
          traditional wet paan, making it convenient for consumption anytime and
          anywhere. Targeted at the premium segment, Rajnigandha stands as the
          world's largest-selling premium pan masala, renowned for its
          consistent and delectable taste. The brand is built on a commitment to
          quality, starting with hand-picked ingredients and advanced processing
          at state-of-the-art facilities in Guwahati, Noida, and Kundli.
          Rajnigandha’s robust distribution network and efficient agents,
          dealers, and retailers across India further support its prominence in
          the market. Passion for perfection and a dedication to excellence have
          established Rajnigandha as a preferred choice for millions of paan
          connoisseurs worldwide. Notably, Rajnigandha is a completely tobacco-
          and nicotine-free pan masala, ensuring a refined and enjoyable
          experience without the associated health risks.
        </h5>
      </span>

      <span className="services-section">
        <h2>Our Chatbot Services</h2>
        <ul>
          <li>
            <strong>Purchase:</strong> Easily buy Rajnigandha Pan Masala online
            or through authorized retailers. Our chatbot can assist you in
            locating products, guiding you through the purchase process, and
            providing product recommendations.
          </li>
          <li>
            <strong>Subscription:</strong> Subscribe for regular deliveries of
            your favorite Rajnigandha products. The chatbot helps you manage
            your subscription preferences, update delivery schedules, and ensure
            you never miss a delivery.
          </li>
          <li>
            <strong>Rewards Program:</strong> Enjoy exclusive offers and rewards
            through our loyalty program. The chatbot can inform you about
            current rewards, help you redeem points, and track your reward
            status.
          </li>
          <li>
            <strong>Account Login:</strong> Access your account to manage
            orders, subscriptions, and rewards. The chatbot provides quick
            assistance with login issues, account updates, and navigating your
            account dashboard.
          </li>
          <li>
            <strong>Order Tracking:</strong> Track the status of your orders in
            real-time. The chatbot keeps you updated on your order’s journey and
            addresses any questions or concerns about shipping and delivery.
          </li>
          <li>
            <strong>Product Search:</strong> Find the specific Rajnigandha
            product you're looking for with our search feature. The chatbot can
            help you find products, filter search results, and provide detailed
            product information.
          </li>
          <li>
            <strong>Shopping Cart:</strong> Manage your selected products and
            proceed to checkout with ease. The chatbot assists with adding items
            to your cart, reviewing cart contents, and completing your purchase.
          </li>
          <li>
            <strong>Customer Support:</strong> Enhance your experience with
            responsive and efficient support. Our chatbot provides instant
            answers to common queries, helps with troubleshooting issues, and
            connects you with human support if needed.
          </li>
        </ul>
      </span>

      <footer className="App-footer">
        <p>© 2023 Dharampal Satyapal Limited. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
