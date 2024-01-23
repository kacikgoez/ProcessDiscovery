export const isInStandaloneMode = () =>
      (window.matchMedia('(display-mode: standalone)').matches) || ('standalone' in window.navigator) || document.referrer.includes('android-app://');

export const capitalizeWords = (sentence : string) => {
      return sentence.split(' ').map(capitalizeFirstLetter).join(' ');
}

export const capitalizeFirstLetter = (word : string) => {
      return word.charAt(0).toUpperCase() + word.slice(1);
}

export const prettyAttributeNames = (attribute : string) => {
      return capitalizeFirstLetter(attribute.replaceAll('_', ' '));
}