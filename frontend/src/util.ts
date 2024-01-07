export const isInStandaloneMode = () =>
      (window.matchMedia('(display-mode: standalone)').matches) || ('standalone' in window.navigator) || document.referrer.includes('android-app://');

export const capitalizeWords = (sentence : string) => {
      return sentence.split(' ').map((word) => {
            return word.charAt(0).toUpperCase() + word.slice(1);
      }).join(' ');
}