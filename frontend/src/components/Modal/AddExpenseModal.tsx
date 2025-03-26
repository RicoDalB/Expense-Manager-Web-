import React, { useState, useEffect } from 'react';
import { fetchCategories, addExpense } from '../../services/api';
import './AddExpenseModal.css';
import CategoryDropdown from '../Categories/CategoryDropdown';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onUpdateData: () => void;
}

const getToday = () => {
  const today = new Date();
  return today.toISOString().split('T')[0];
};

const AddExpenseModal: React.FC<Props> = ({ isOpen, onClose, onUpdateData }) => {
  const [formData, setFormData] = useState({
    title: '',
    amount: '',
    date: getToday(),
    category: ''
  });
  const [categories, setCategories] = useState([]);
  const [loadingCategories, setLoadingCategories] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCategories = async () => {
      try {
        const data = await fetchCategories();
        setCategories(data);
      } catch (error) {
        console.error('❌ Errore nel caricamento categorie:', error);
        setError('Errore nel caricamento delle categorie.');
      } finally {
        setLoadingCategories(false);
      }
    };

    loadCategories();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const payload = {
      description: formData.title,
      amount: parseFloat(formData.amount),
      date: formData.date,
      category_id: parseInt(formData.category),
    };

    try {
      await addExpense(payload); // Funzione che invia la spesa al backend
      setFormData({ title: '', amount: '', date: getToday(), category: '' }); // Reset dei dati dopo salvataggio
      onUpdateData(); //notifica aggiornamento
      onClose(); // Chiudi il modal
    } catch (err) {
      console.error('Errore nel salvataggio della spesa', err);
      setError('Errore durante il salvataggio');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <h2 className="modal-title">Aggiungi una Spesa</h2>

        {error && <p className="modal-error">{error}</p>}

        <form onSubmit={handleSubmit} className="modal-form">
          <input
            type="text"
            name="title"
            placeholder="Titolo"
            value={formData.title}
            onChange={handleChange}
            required
          />

          <input
            type="number"
            name="amount"
            placeholder="Importo (€)"
            value={formData.amount}
            onChange={handleChange}
            required
          />

          <input
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            required
          />

          {loadingCategories ? (
            <p>Caricamento categorie...</p>
          ) : (
            <CategoryDropdown
              categories={categories}
              selectedId={formData.category}
              onChange={(value) => setFormData({ ...formData, category: value })}
            />
          )}

          <div className="modal-action">
            <button type="button" onClick={onClose} className="cancel-btn">Annulla</button>
            <button type="submit" className="save-btn">Salva</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddExpenseModal;
