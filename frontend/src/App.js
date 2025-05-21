import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  HomeIcon, 
  MapPinIcon, 
  CurrencyDollarIcon, 
  ArrowsPointingOutIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';

function App() {
  const [ilanlar, setIlanlar] = useState([]);
  const [filteredIlanlar, setFilteredIlanlar] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    minPrice: '',
    maxPrice: '',
    odaSayisi: '',
    minMetrekare: '',
    maxMetrekare: ''
  });

  useEffect(() => {
    fetchIlanlar();
  }, []);

  useEffect(() => {
    filterIlanlar();
  }, [ilanlar, searchTerm, filters]);

  const fetchIlanlar = async () => {
    try {
      const response = await axios.get('http://localhost:8000/ilan');
      setIlanlar(response.data);
      setFilteredIlanlar(response.data);
      setLoading(false);
    } catch (err) {
      setError('İlanlar yüklenirken bir hata oluştu.');
      setLoading(false);
    }
  };

  const filterIlanlar = () => {
    let filtered = [...ilanlar];

    // Arama filtresi
    if (searchTerm) {
      filtered = filtered.filter(ilan => 
        ilan.baslik.toLowerCase().includes(searchTerm.toLowerCase()) ||
        ilan.aciklama.toLowerCase().includes(searchTerm.toLowerCase()) ||
        ilan.mahalle.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Fiyat filtresi
    if (filters.minPrice) {
      filtered = filtered.filter(ilan => ilan.fiyat >= Number(filters.minPrice));
    }
    if (filters.maxPrice) {
      filtered = filtered.filter(ilan => ilan.fiyat <= Number(filters.maxPrice));
    }

    // Oda sayısı filtresi
    if (filters.odaSayisi) {
      filtered = filtered.filter(ilan => ilan.oda_sayisi === filters.odaSayisi);
    }

    // Metrekare filtresi
    if (filters.minMetrekare) {
      filtered = filtered.filter(ilan => ilan.metrekare >= Number(filters.minMetrekare));
    }
    if (filters.maxMetrekare) {
      filtered = filtered.filter(ilan => ilan.metrekare <= Number(filters.maxMetrekare));
    }

    setFilteredIlanlar(filtered);
  };

  const clearFilters = () => {
    setFilters({
      minPrice: '',
      maxPrice: '',
      odaSayisi: '',
      minMetrekare: '',
      maxMetrekare: ''
    });
    setSearchTerm('');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-red-600">{error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">Emlak İlanları</h1>
            <div className="flex items-center space-x-4">
              <div className="relative">
                <input
                  type="text"
                  placeholder="İlan ara..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400 absolute left-3 top-2.5" />
              </div>
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="flex items-center px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                <FunnelIcon className="h-5 w-5 mr-2" />
                Filtrele
              </button>
            </div>
          </div>

          {/* Filtreler */}
          {showFilters && (
            <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold">Filtreler</h2>
                <button
                  onClick={clearFilters}
                  className="text-sm text-gray-600 hover:text-gray-900"
                >
                  Filtreleri Temizle
                </button>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Min. Fiyat</label>
                  <input
                    type="number"
                    value={filters.minPrice}
                    onChange={(e) => setFilters({...filters, minPrice: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    placeholder="Min. Fiyat"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Max. Fiyat</label>
                  <input
                    type="number"
                    value={filters.maxPrice}
                    onChange={(e) => setFilters({...filters, maxPrice: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    placeholder="Max. Fiyat"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Oda Sayısı</label>
                  <select
                    value={filters.odaSayisi}
                    onChange={(e) => setFilters({...filters, odaSayisi: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  >
                    <option value="">Tümü</option>
                    <option value="1+1">1+1</option>
                    <option value="2+1">2+1</option>
                    <option value="3+1">3+1</option>
                    <option value="4+1">4+1</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Min. m²</label>
                  <input
                    type="number"
                    value={filters.minMetrekare}
                    onChange={(e) => setFilters({...filters, minMetrekare: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    placeholder="Min. m²"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Max. m²</label>
                  <input
                    type="number"
                    value={filters.maxMetrekare}
                    onChange={(e) => setFilters({...filters, maxMetrekare: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    placeholder="Max. m²"
                  />
                </div>
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredIlanlar.map((ilan) => (
            <div key={ilan.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
              {/* İlan Detayları */}
              <div className="p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-3">{ilan.baslik}</h2>
                <p className="text-gray-600 mb-4 line-clamp-2">{ilan.aciklama}</p>

                {/* İlan Özellikleri */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="flex items-center text-gray-600">
                    <MapPinIcon className="h-5 w-5 mr-2" />
                    <span>{ilan.mahalle}</span>
                  </div>
                  <div className="flex items-center text-gray-600">
                    <HomeIcon className="h-5 w-5 mr-2" />
                    <span>{ilan.oda_sayisi}</span>
                  </div>
                  <div className="flex items-center text-gray-600">
                    <ArrowsPointingOutIcon className="h-5 w-5 mr-2" />
                    <span>{ilan.metrekare} m²</span>
                  </div>
                  <div className="flex items-center text-primary-600 font-semibold">
                    <CurrencyDollarIcon className="h-5 w-5 mr-2" />
                    <span>{ilan.fiyat?.toLocaleString('tr-TR')} TL</span>
                  </div>
                </div>

                {/* Detay Butonu */}
                <a
                  href={ilan.drive_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full text-center bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 transition-colors duration-300"
                >
                  Detayları Gör
                </a>
              </div>
            </div>
          ))}
        </div>

        {/* Sonuç Bulunamadı */}
        {filteredIlanlar.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">Arama kriterlerinize uygun ilan bulunamadı.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App; 