import React from "react";
import { Listbox } from "@headlessui/react";
import "./CategoryDropdown.css";

interface Category {
  id: number;
  name: string;
  icon: string;
}

interface Props {
  categories: Category[];
  selectedId: string;
  onChange: (value: string) => void;
}

const CategoryDropdown: React.FC<Props> = ({ categories, selectedId, onChange }) => {
  const selected = categories.find((c) => c.id === parseInt(selectedId));

  const getIconUrl = (icon: string) => {
  if (!icon) return "/placeholder.png";

  // Se l'URL inizia già con http (già completo), restituiscilo così com'è
  if (icon.startsWith("http://") || icon.startsWith("https://")) {
    return icon;
  }

  // Altrimenti costruiamo l'URL aggiungendo .png se manca
  const cleanIcon = icon.endsWith(".png") ? icon : `${icon}.png`;
  return `http://127.0.0.1:8000/icons/${cleanIcon}`;
};

  return (
    <div className="dropdown-wrapper">
      <Listbox value={selectedId} onChange={onChange}>
        <Listbox.Button className="dropdown-button">
          {selected ? (
            <div className="dropdown-selected">
              <img
                src={getIconUrl(selected.icon)}
                alt={selected.name}
                className="dropdown-icon"
                onError={(e) => {
                  e.currentTarget.src = "/placeholder.png";
                }}
              />
              <span>{selected.name}</span>
            </div>
          ) : (
            <span className="dropdown-placeholder">Seleziona Categoria</span>
          )}
        </Listbox.Button>

        <Listbox.Options className="dropdown-options">
          {categories.map((cat) => (
            <Listbox.Option
              key={cat.id}
              value={cat.id.toString()}
              className={({ active }) =>
                `dropdown-option ${active ? "dropdown-option-active" : ""}`
              }
            >
              <img
                src={getIconUrl(cat.icon)}
                alt={cat.name}
                className="dropdown-icon"
                onError={(e) => {
                  e.currentTarget.src = "/placeholder.png";
                }}
              />
              <span>{cat.name}</span>
            </Listbox.Option>
          ))}
        </Listbox.Options>
      </Listbox>
    </div>
  );
};

export default CategoryDropdown;