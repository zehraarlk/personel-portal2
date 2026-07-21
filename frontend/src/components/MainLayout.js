import Navbar from './Navbar';
import Footer from './Footer';
import Breadcrumb from './Breadcrumb';

export default function MainLayout({ title, crumbs, children }) {
  return (
    <div className="app-shell">
      <Navbar />
      <Breadcrumb title={title} crumbs={crumbs} />
      <main className="content-area">
        <div className="page-inner">{children}</div>
      </main>
      <Footer />
    </div>
  );
}
