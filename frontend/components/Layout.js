import Link from 'next/link';
import { useEffect, useState } from 'react';

const menu = [
  { href: '/factories', label: 'Factories' },
  { href: '/product-nodes', label: 'Product Nodes' },
  { href: '/params', label: 'Parameters Catalog' },
  { href: '/params-product-nodes', label: 'Params per Node' },
  { href: '/accessories', label: 'Accessories' },
  { href: '/skus', label: 'SKU (Customer Models)' },
  { href: '/supplier-models', label: 'Supplier Models' },
  { href: '/links', label: 'Links (Candidates)' },
  { href: '/compare-tables', label: 'Compare Tables' },
  { href: '/contracts', label: 'Contracts & Tech Tasks' },
];

export default function Layout({ children, title }) {
  const [role, setRole] = useState('BM');

  useEffect(() => {
    const stored = window.localStorage.getItem('role');
    if (stored) setRole(stored);
  }, []);

  const updateRole = (event) => {
    setRole(event.target.value);
    window.localStorage.setItem('role', event.target.value);
  };

  return (
    <div className="layout">
      <aside className="sidebar">
        <h2>MVP Menu</h2>
        {menu.map((item) => (
          <Link key={item.href} href={item.href}>
            {item.label}
          </Link>
        ))}
      </aside>
      <div className="content">
        <header className="header">
          <div>{title}</div>
          <div className="flex">
            <span className="badge">Role</span>
            <select className="role-select" value={role} onChange={updateRole}>
              <option value="BM">BM</option>
              <option value="PM">PM</option>
              <option value="Engineer">Engineer</option>
            </select>
          </div>
        </header>
        <main className="page">{children}</main>
      </div>
    </div>
  );
}
