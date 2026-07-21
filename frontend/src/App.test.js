import { render, screen } from '@testing-library/react';
import App from './App';

test('renders portal brand', () => {
  render(<App />);
  expect(screen.getByText(/Gebze Belediyesi/i)).toBeInTheDocument();
});
