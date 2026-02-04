import Layout from '../components/Layout';

export default function Home() {
  return (
    <Layout title="MVP Dashboard">
      <div className="card">
        <h3>Welcome</h3>
        <p>Use the left menu to navigate through the MVP modules.</p>
        <p>The role selector in the header simulates BM / PM / Engineer access.</p>
      </div>
    </Layout>
  );
}
