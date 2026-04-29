import { Component, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ApiService } from '../../services/api.service';

// ======================================================
// INTERFACES
// ======================================================

interface HistoryItem {
  id: number;
  generation_type: 'text' | 'image' | 'video';
  prompt: string;
  style?: string;
  result?: string;
  created_at: string;
}

interface GenerationType {
  id: 'text' | 'image' | 'video';
  label: string;
  icon: string;
  description: string;
}

// ======================================================
// COMPOSANT
// ======================================================

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  // ======================================================
  // ÉTAT DE L'APPLICATION
  // ======================================================

  // Prompt entré par l'utilisateur
  prompt = '';

  // Style sélectionné pour les images
  selectedStyle = 'general';

  // Type de génération sélectionné
  selectedType = signal<'text' | 'image' | 'video'>('text');

  // États de chargement
  isGenerating = signal(false);
  isLoadingHistory = signal(false);

  // Résultats
  textResult = signal('');
  imageResult = signal('');
  videoUrl = signal('');

  // Messages
  errorMessage = signal('');
  successMessage = signal('');

  // Historique
  history = signal<HistoryItem[]>([]);
  selectedHistoryItem = signal<HistoryItem | null>(null);

  // Sidebar
  isSidebarOpen = signal(true);

  // ======================================================
  // DONNÉES STATIQUES
  // ======================================================

  generationTypes: GenerationType[] = [
    {
      id: 'text',
      label: 'Texte',
      icon: '📝',
      description: 'Générer du texte avec LLaMA 3.3'
    },
    {
      id: 'image',
      label: 'Image',
      icon: '🖼️',
      description: 'Créer des images avec FLUX.1'
    },
    {
      id: 'video',
      label: 'Vidéo',
      icon: '🎬',
      description: 'Produire des vidéos cinématiques'
    }
  ];

  imageStyles = [
    { value: 'general', label: '🎨 Général' },
    { value: 'photo', label: '📷 Photo' },
    { value: 'art', label: '🖌️ Art' },
    { value: 'anime', label: '🎌 Anime' },
    { value: 'cinematic', label: '🎬 Cinématique' },
    { value: 'fantasy', label: '🧙 Fantasy' },
    { value: 'realistic', label: '🌍 Réaliste' }
  ];

  // ======================================================
  // CONSTRUCTOR
  // ======================================================

  constructor(
    public authService: AuthService,
    private apiService: ApiService,
    private router: Router
  ) {}

  // ======================================================
  // INITIALISATION
  // ======================================================

  ngOnInit(): void {
    this.loadHistory();
  }

  // ======================================================
  // GÉNÉRATION
  // ======================================================

  generate(): void {
    if (!this.prompt.trim()) {
      this.errorMessage.set('Veuillez entrer un prompt');
      return;
    }

    this.isGenerating.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');
    this.textResult.set('');
    this.imageResult.set('');
    this.videoUrl.set('');

    const type = this.selectedType();

    if (type === 'text') {
      this.generateText();
    } else if (type === 'image') {
      this.generateImage();
    } else {
      this.generateVideo();
    }
  }

  private generateText(): void {
    this.apiService.generateText(this.prompt).subscribe({
      next: (response) => {
        this.textResult.set(response.result);
        this.isGenerating.set(false);
        this.successMessage.set('Texte généré avec succès !');
        this.loadHistory();
      },
      error: (err) => {
        this.isGenerating.set(false);
        this.errorMessage.set(err.message || 'Erreur de génération');
      }
    });
  }

  private generateImage(): void {
    this.apiService.generateImage(this.prompt, this.selectedStyle).subscribe({
      next: (response) => {
        this.imageResult.set(response.result);
        this.isGenerating.set(false);
        this.successMessage.set('Image générée avec succès !');
        this.loadHistory();
      },
      error: (err) => {
        this.isGenerating.set(false);
        this.errorMessage.set(err.message || 'Erreur de génération');
      }
    });
  }

  private generateVideo(): void {
    this.apiService.generateVideo(this.prompt).subscribe({
      next: (blob) => {
        const url = URL.createObjectURL(blob);
        this.videoUrl.set(url);
        this.isGenerating.set(false);
        this.successMessage.set('Vidéo générée avec succès !');
        this.loadHistory();
      },
      error: (err) => {
        this.isGenerating.set(false);
        this.errorMessage.set(err.message || 'Erreur de génération');
      }
    });
  }

  // ======================================================
  // HISTORIQUE
  // ======================================================

  loadHistory(): void {
    this.isLoadingHistory.set(true);
    this.apiService.getHistory().subscribe({
      next: (response) => {
        this.history.set(response.items);
        this.isLoadingHistory.set(false);
      },
      error: () => {
        this.isLoadingHistory.set(false);
      }
    });
  }

  selectHistoryItem(item: HistoryItem): void {
    this.selectedHistoryItem.set(item);
    this.prompt = item.prompt;
    this.selectedType.set(item.generation_type);

    // Affiche le résultat
    if (item.generation_type === 'text') {
      this.textResult.set(item.result || '');
      this.imageResult.set('');
      this.videoUrl.set('');
    } else if (item.generation_type === 'image') {
      this.imageResult.set(item.result || '');
      this.textResult.set('');
      this.videoUrl.set('');
      if (item.style) this.selectedStyle = item.style;
    }

    this.errorMessage.set('');
    this.successMessage.set('');
  }

  deleteHistoryItem(id: number, event: Event): void {
    event.stopPropagation();
    this.apiService.deleteHistory(id).subscribe({
      next: () => {
        this.history.update(items => items.filter(i => i.id !== id));
        if (this.selectedHistoryItem()?.id === id) {
          this.selectedHistoryItem.set(null);
        }
      },
      error: () => {}
    });
  }

  // ======================================================
  // UI HELPERS
  // ======================================================

  selectType(type: 'text' | 'image' | 'video'): void {
    this.selectedType.set(type);
    this.textResult.set('');
    this.imageResult.set('');
    this.videoUrl.set('');
    this.errorMessage.set('');
    this.successMessage.set('');
  }

  toggleSidebar(): void {
    this.isSidebarOpen.update(v => !v);
  }

  logout(): void {
    this.authService.logout();
  }

  getTypeIcon(type: string): string {
    const icons: Record<string, string> = {
      text: '📝',
      image: '🖼️',
      video: '🎬'
    };
    return icons[type] || '📝';
  }

  formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  downloadImage(): void {
    const link = document.createElement('a');
    link.href = this.imageResult();
    link.download = 'generated-image.png';
    link.click();
  }

  getLoadingMessage(): string {
    const messages: Record<string, string> = {
      text: 'Génération du texte...',
      image: 'Création de l\'image (~15s)...',
      video: 'Production de la vidéo (~60s)...'
    };
    return messages[this.selectedType()] || 'Génération...';
  }
}