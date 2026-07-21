import { Link } from 'react-router-dom';
import './Breadcrumb.css';

export default function Breadcrumb({ title, crumbs }) {
  const items = crumbs || [{ label: 'Ana Sayfa', to: '/' }, { label: title }];

  return (
    <div className="breadcrumb-bar">
      <div className="breadcrumb-container">
        <nav aria-label="breadcrumb">
          <ol>
            {items.map((item, index) => {
              const isLast = index === items.length - 1;
              return (
                <li
                  key={`${item.label}-${index}`}
                  aria-current={isLast ? 'page' : undefined}
                >
                  {item.to && !isLast ? (
                    <Link to={item.to}>{item.label}</Link>
                  ) : (
                    item.label
                  )}
                </li>
              );
            })}
          </ol>
        </nav>
      </div>
    </div>
  );
}
