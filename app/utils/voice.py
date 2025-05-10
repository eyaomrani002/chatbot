<script>
const translations = {
    fr: {
        title: "Chatbot ISET",
        historyLabel: "Historique",
        clearHistoryLabel: "Effacer",
        pdfLabel: "Téléverser un PDF",
        imageLabel: "Téléverser une image",
        outputLangLabel: "Langue de la réponse",
        voiceLabel: "Utiliser la voix",
        exportLabel: "Exporter en PDF",
        responsePrompt: "Aidez-nous à améliorer ! Fournissez une réponse correcte :",
        placeholder: "Posez votre question...",
        newResponse: "Entrez la réponse correcte...",
        newLink: "Lien (optionnel)...",
        submit: "Soumettre",
        noMatch: "Désolé, je n'ai pas compris.",
        error: "Erreur",
        speechNotSupported: "La reconnaissance vocale n'est pas supportée par ce navigateur.",
        speechError: "Échec de la reconnaissance vocale.",
        recording: "Enregistrement...",
        uploading: "Téléversement",
        networkError: "Erreur réseau",
        fileUploaded: "Fichier uploadé",
        responseAdded: "Merci ! Votre réponse a été ajoutée.",
        noResponse: "Veuillez entrer une réponse.",
        historyCleared: "Historique vidé.",
        noConversations: "Aucune conversation à exporter.",
        exportSuccess: "PDF exporté avec succès.",
        exporting: "Exportation...",
        textExtracted: "Texte extrait prêt à envoyer",
        previewLabel: "Aperçu du texte extrait :"
    },
    en: {
        title: "ISET Chatbot",
        historyLabel: "History",
        clearHistoryLabel: "Clear",
        pdfLabel: "Upload a PDF",
        imageLabel: "Upload an image",
        outputLangLabel: "Response language",
        voiceLabel: "Use voice",
        exportLabel: "Export to PDF",
        responsePrompt: "Help us improve! Provide a correct answer:",
        placeholder: "Ask your question...",
        newResponse: "Enter the correct answer...",
        newLink: "Link (optional)...",
        submit: "Submit",
        noMatch: "Sorry, I didn't understand.",
        error: "Error",
        speechNotSupported: "Speech recognition is not supported by this browser.",
        speechError: "Speech recognition failed.",
        recording: "Recording...",
        uploading: "Uploading",
        networkError: "Network error",
        fileUploaded: "File uploaded",
        responseAdded: "Thank you! Your response has been added.",
        noResponse: "Please enter a response.",
        historyCleared: "History cleared.",
        noConversations: "No conversations to export.",
        exportSuccess: "PDF exported successfully.",
        exporting: "Exporting...",
        textExtracted: "Extracted text ready to send",
        previewLabel: "Preview of extracted text :"
    },
    ar: {
        title: "روبوت الدردشة ISET",
        historyLabel: "السجل",
        clearHistoryLabel: "مسح",
        pdfLabel: "تحميل ملف PDF",
        imageLabel: "تحميل صورة",
        outputLangLabel: "لغة الرد",
        voiceLabel: "استخدام الصوت",
        exportLabel: "تصدير إلى PDF",
        responsePrompt: "ساعدنا على التحسين! قدم إجابة صحيحة:",
        placeholder: "اطرح سؤالك...",
        newResponse: "أدخل الإجابة الصحيحة...",
        newLink: "رابط (اختياري)...",
        submit: "إرسال",
        noMatch: "عذرًا، لم أفهم.",
        error: "خطأ",
        speechNotSupported: "التعرف على الكلام غير مدعوم في هذا المتصفح.",
        speechError: "فشل التعرف على الكلام.",
        recording: "جارٍ التسجيل...",
        uploading: "جارٍ الرفع",
        networkError: "خطأ في الشبكة",
        fileUploaded: "تم رفع الملف",
        responseAdded: "شكرًا! تمت إضافة ردك.",
        noResponse: "يرجى إدخال رد.",
        historyCleared: "تم مسح السجل.",
        noConversations: "لا توجد محادثات للتصدير.",
        exportSuccess: "تم تصدير PDF بنجاح.",
        exporting: "جارٍ التصدير...",
        textExtracted: "النص المستخرج جاهز للإرسال",
        previewLabel: "معاينة النص المستخرج :"
    }
};

const errorMessages = {
    'Aucune question ou fichier fourni': {
        fr: 'Veuillez entrer une question ou téléverser un fichier.',
        en: 'Please enter a question or upload a file.',
        ar: 'يرجى إدخال سؤال أو رفع ملف.'
    },
    'Fichier PDF invalide': {
        fr: 'Le fichier doit être un PDF valide.',
        en: 'The file must be a valid PDF.',
        ar: 'يجب أن يكون الملف بصيغة PDF صالحة.'
    },
    'Fichier image invalide (PNG/JPEG requis)': {
        fr: 'Seuls les fichiers PNG ou JPEG sont acceptés.',
        en: 'Only PNG or JPEG files are accepted.',
        ar: 'يتم قبول ملفات PNG أو JPEG فقط.'
    },
    'Fichier PDF trop volumineux (max 5 Mo)': {
        fr: 'Le PDF dépasse la limite de 5 Mo.',
        en: 'The PDF exceeds the 5 MB limit.',
        ar: 'يتجاوز ملف PDF حد 5 ميغابايت.'
    },
    'Fichier image trop volumineux (max 5 Mo)': {
        fr: 'L’image dépasse la limite de 5 Mo.',
        en: 'The image exceeds the 5 MB limit.',
        ar: 'تتجاوز الصورة حد 5 ميغابايت.'
    },
    'Aucune donnée disponible pour répondre.': {
        fr: 'Désolé, je n\'ai pas compris.',
        en: 'Sorry, I didn\'t understand.',
        ar: 'عذرًا، لم أفهم.'
    },
    'Aucun texte détecté dans le PDF.': {
        fr: 'Aucun texte détecté dans le PDF.',
        en: 'No text detected in the PDF.',
        ar: 'لم يتم الكشف عن نص في ملف PDF.'
    },
    'Erreur lors de l\'extraction du texte.': {
        fr: 'Erreur lors de l\'extraction du texte.',
        en: 'Error during text extraction.',
        ar: 'خطأ أثناء استخراج النص.'
    },
    'Fichier PDF introuvable.': {
        fr: 'Fichier PDF introuvable. Vérifiez le fichier téléversé.',
        en: 'PDF file not found. Check the uploaded file.',
        ar: 'ملف PDF غير موجود. تحقق من الملف المرفوع.'
    },
    'Erreur : type de fichier non supporté.': {
        fr: 'Seuls les fichiers PDF ou PNG/JPEG sont acceptés.',
        en: 'Only PDF or PNG/JPEG files are accepted.',
        ar: 'يتم قبول ملفات PDF أو PNG/JPEG فقط.'
    },
    'Aucun texte détecté dans l\'image.': {
        fr: 'Aucun texte détecté dans l\'image.',
        en: 'No text detected in the image.',
        ar: 'لم يتم الكشف عن نص في الصورة.'
    },
    'Fichier image introuvable.': {
        fr: 'Fichier image introuvable. Vérifiez le fichier téléversé.',
        en: 'Image file not found. Check the uploaded file.',
        ar: 'ملف الصورة غير موجود. تحقق من الملف المرفوع.'
    }
};

const chatbox = document.getElementById('chatbox');
const historyBox = document.getElementById('historyBox');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const recordButton = document.getElementById('recordButton');
const historyButton = document.getElementById('historyButton');
const exportButton = document.getElementById('exportButton');
const responseForm = document.getElementById('responseForm');
const newResponse = document.getElementById('newResponse');
const newLink = document.getElementById('newLink');
const newCategory = document.getElementById('newCategory');
const submitResponse = document.getElementById('submitResponse');
const uiLang = document.getElementById('ui_lang');
const micStatus = document.getElementById('micStatus');
const previewBox = document.getElementById('previewBox');

let recognition;
let isRecognizing = false;

let conversations = JSON.parse(localStorage.getItem('conversations')) || [];

function escapeHTML(str) {
    if (typeof str !== 'string' || str == null) {
        return '';
    }
    return str.replace(/[&<>"']/g, match => ({
        '&': '&',
        '<': '<',
        '>': '>',
        '"': '"',
        "'": '''
    }[match]));
}

function getTranslation(key, lang, fallback = key) {
    const validLang = translations[lang] ? lang : 'fr';
    return translations[validLang][key] || translations['fr'][key] || fallback;
}

// Gestion de l'upload de PDF
document.getElementById('pdf_file').addEventListener('change', async (e) => {
    const label = document.getElementById('pdfLabel');
    const clearBtn = document.getElementById('clearPdf');
    const pdfFile = e.target.files[0];

    if (pdfFile) {
        label.textContent = `${getTranslation('pdfLabel', uiLang.value).split(':')[0]} : ${pdfFile.name}`;
        clearBtn.classList.remove('hidden');

        try {
            const formData = new FormData();
            formData.append('pdf_file', pdfFile);
            formData.append('output_lang', 'fr');
            formData.append('csrf_token', document.getElementById('csrf_token').value);

            addMessage(`${getTranslation('uploading', uiLang.value)}...`, false);
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.getElementById('csrf_token').value
                },
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.extracted_text || errorData.error || getTranslation('networkError', uiLang.value));
            }

            const data = await response.json();
            console.log('Réponse /chat pour PDF:', data);
            if (data.error) {
                addMessage(`${getTranslation('error', uiLang.value)} : ${errorMessages[data.error]?.[uiLang.value] || data.error}`, false);
                return;
            }

            const extractedText = data.extracted_text || '';
            if (extractedText && ![
                "Aucun texte détecté dans le PDF.",
                "Erreur lors de l'extraction du texte.",
                "Fichier PDF introuvable.",
                "Erreur : type de fichier non supporté."
            ].includes(extractedText)) {
                previewBox.innerHTML = `<strong>${getTranslation('previewLabel', uiLang.value)}</strong><br>${escapeHTML(extractedText.slice(0, 500))}${extractedText.length > 500 ? '...' : ''}`;
                previewBox.classList.remove('hidden');
                userInput.value = extractedText.trim().slice(0, 1000);
                toggleCancelButton();
                addMessage(`${getTranslation('textExtracted', uiLang.value)}`, false);
            } else {
                addMessage(`${getTranslation('error', uiLang.value)} : ${errorMessages[extractedText]?.[uiLang.value] || extractedText || getTranslation('noTextExtracted', uiLang.value)}`, false);
                previewBox.classList.add('hidden');
                return;
            }

        } catch (error) {
            addMessage(`${getTranslation('error', uiLang.value)} : ${error.message}`, false);
            console.error('Erreur lors de l\'upload de PDF:', error);
            previewBox.classList.add('hidden');
        }
    } else {
        label.textContent = getTranslation('pdfLabel', uiLang.value);
        clearBtn.classList.add('hidden');
        userInput.value = '';
        previewBox.classList.add('hidden');
        toggleCancelButton();
    }
});

// Gestion de l'upload d'image
document.getElementById('image_file').addEventListener('change', async (e) => {
    const label = document.getElementById('imageLabel');
    const clearBtn = document.getElementById('clearImage');
    const imageFile = e.target.files[0];

    if (imageFile) {
        label.textContent = `${getTranslation('imageLabel', uiLang.value).split(':')[0]} : ${imageFile.name}`;
        clearBtn.classList.remove('hidden');

        const reader = new FileReader();
        reader.onload = (event) => {
            const img = document.createElement('img');
            img.src = event.target.result;
            img.className = 'mt-2 max-w-full rounded-lg';
            img.style.maxHeight = '100px';
            chatbox.appendChild(img);
            chatbox.scrollTop = chatbox.scrollHeight;
        };
        reader.readAsDataURL(imageFile);

        try {
            const formData = new FormData();
            formData.append('image_file', imageFile);
            formData.append('output_lang', 'fr');
            formData.append('csrf_token', document.getElementById('csrf_token').value);

            addMessage(`${getTranslation('uploading', uiLang.value)}...`, false);
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.getElementById('csrf_token').value
                },
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.extracted_text || errorData.error || getTranslation('networkError', uiLang.value));
            }

            const data = await response.json();
            console.log('Réponse /chat pour image:', data);
            if (data.error) {
                addMessage(`${getTranslation('error', uiLang.value)} : ${errorMessages[data.error]?.[uiLang.value] || data.error}`, false);
                return;
            }

            const extractedText = data.extracted_text || '';
            if (extractedText && ![
                "Aucun texte détecté dans l'image.",
                "Erreur lors de l'extraction du texte.",
                "Fichier image introuvable.",
                "Erreur : type de fichier non supporté."
            ].includes(extractedText)) {
                previewBox.innerHTML = `<strong>${getTranslation('previewLabel', uiLang.value)}</strong><br>${escapeHTML(extractedText.slice(0, 500))}${extractedText.length > 500 ? '...' : ''}`;
                previewBox.classList.remove('hidden');
                userInput.value = extractedText.trim().slice(0, 1000);
                toggleCancelButton();
                addMessage(`${getTranslation('textExtracted', uiLang.value)}`, false);
            } else {
                addMessage(`${getTranslation('error', uiLang.value)} : ${errorMessages[extractedText]?.[uiLang.value] || extractedText || getTranslation('noTextExtracted', uiLang.value)}`, false);
                previewBox.classList.add('hidden');
                return;
            }

        } catch (error) {
            addMessage(`${getTranslation('error', uiLang.value)} : ${error.message}`, false);
            console.error('Erreur lors de l\'upload d\'image:', error);
            previewBox.classList.add('hidden');
        }
    } else {
        label.textContent = getTranslation('imageLabel', uiLang.value);
        clearBtn.classList.add('hidden');
        userInput.value = '';
        previewBox.classList.add('hidden');
        toggleCancelButton();
    }
});

document.getElementById('clearPdf').addEventListener('click', () => {
    document.getElementById('pdf_file').value = '';
    document.getElementById('pdfLabel').textContent = getTranslation('pdfLabel', uiLang.value);
    document.getElementById('clearPdf').classList.add('hidden');
    userInput.value = '';
    previewBox.classList.add('hidden');
    toggleCancelButton();
});

document.getElementById('clearImage').addEventListener('click', () => {
    document.getElementById('image_file').value = '';
    document.getElementById('imageLabel').textContent = getTranslation('imageLabel', uiLang.value);
    document.getElementById('clearImage').classList.add('hidden');
    userInput.value = '';
    previewBox.classList.add('hidden');
    toggleCancelButton();
});

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    stopRecognition();

    const formData = new FormData(chatForm);
    const message = userInput.value.trim();
    const pdfFile = formData.get('pdf_file');
    const imageFile = formData.get('image_file');

    if (!message && !pdfFile.name && !imageFile.name) {
        addMessage(errorMessages['Aucune question ou fichier fourni'][uiLang.value] || getTranslation('noQuestionOrFile', uiLang.value), false);
        return;
    }

    if (pdfFile.name && (pdfFile.size > 5 * 1024 * 1024 || !pdfFile.name.endsWith('.pdf'))) {
        addMessage(errorMessages['Fichier PDF invalide'][uiLang.value] || getTranslation('invalidPDF', uiLang.value), false);
        return;
    }
    if (imageFile.name && (imageFile.size > 5 * 1024 * 1024 || !['image/png', 'image/jpeg'].includes(imageFile.type))) {
        addMessage(errorMessages['Fichier image invalide (PNG/JPEG requis)'][uiLang.value] || getTranslation('invalidImage', uiLang.value), false);
        return;
    }

    console.log('Message envoyé:', message);
    sendButton.disabled = true;
    sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

    if (message) {
        addMessage(message, true);
        previewBox.classList.add('hidden');
    }

    try {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/chat', true);
        xhr.upload.onprogress = (event) => {
            if (event.lengthComputable) {
                const percent = (event.loaded / event.total) * 100;
                addMessage(`${getTranslation('uploading', uiLang.value)} : ${Math.round(percent)}%`, false);
            }
        };
        xhr.onload = () => {
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);
                console.log('Réponse /chat pour message:', data);
                if (data.error) {
                    throw new Error(errorMessages[data.error]?.[uiLang.value] || data.error);
                }
                const conversation = {
                    question: message || getTranslation('fileUploaded', uiLang.value),
                    answer: data.answer || getTranslation('noMatch', uiLang.value),
                    link: data.link || '',
                    category: data.category || 'Général',
                    response_id: data.response_id || '',
                    rating: 'Non évalué'
                };
                conversations.push(conversation);
                if (conversations.length > 100) conversations = conversations.slice(-100);
                localStorage.setItem('conversations', JSON.stringify(conversations));
                addMessage(data.answer, false, data);
                updateHistory();
                if (data.ask_for_response || data.confidence < 0.3) {
                    responseForm.classList.remove('hidden');
                    responseForm.dataset.question = message || getTranslation('fileUploaded', uiLang.value);
                }
                if (chatbox.querySelector('.chat-bubble-bot')?.textContent.includes('Chargement')) {
                    chatbox.querySelector('.chat-bubble-bot').remove();
                }
            } else {
                const errorData = JSON.parse(xhr.responseText);
                throw new Error(errorMessages[errorData.error]?.[uiLang.value] || errorData.error || getTranslation('networkError', uiLang.value));
            }
        };
        xhr.onerror = () => {
            throw new Error(getTranslation('networkError', uiLang.value));
        };
        xhr.send(formData);
    } catch (error) {
        addMessage(`${getTranslation('error', uiLang.value)} : ${error.message}`, false);
        console.error('Erreur chat:', error);
    } finally {
        sendButton.disabled = false;
        sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        userInput.value = '';
        previewBox.classList.add('hidden');
        toggleCancelButton();
    }
});

function addMessage(content, isUser, data = {}) {
    const div = document.createElement('div');
    div.className = isUser ? 'chat-bubble-user' : 'chat-bubble-bot';
    div.setAttribute('role', 'region');
    div.setAttribute('aria-live', 'polite');
    if (isUser) {
        div.textContent = escapeHTML(content);
    } else {
        const contentDiv = document.createElement('div');
        const displayAnswer = escapeHTML(content) || translations[uiLang.value].noMatch;
        contentDiv.innerHTML = `<strong>Chatbot :</strong> ${displayAnswer}`;
        if (data.extracted_text) {
            contentDiv.innerHTML += `<br><strong>Contenu extrait :</strong> ${escapeHTML(data.extracted_text)}`;
        }
        if (data.link && isValidURL(data.link)) {
            const link = document.createElement('a');
            link.href = escapeHTML(data.link);
            link.className = 'text-blue-500 underline';
            link.target = '_blank';
            link.textContent = translations[uiLang.value].link || 'Lien';
            contentDiv.appendChild(document.createElement('br'));
            contentDiv.appendChild(link);
        }
        if (data.audio) {
            const audio = document.createElement('audio');
            audio.controls = true;
            audio.src = data.audio;
            audio.onerror = () => addMessage("Erreur : Impossible de lire l'audio.", false);
            contentDiv.appendChild(document.createElement('br'));
            contentDiv.appendChild(audio);
        }
        if (data.response_id) {
            const ratingDiv = document.createElement('div');
            ratingDiv.className = 'mt-2';
            ratingDiv.innerHTML = `
                <button class="like-btn text-green-500 hover:text-green-700" data-id="${data.response_id}"><i class="fas fa-thumbs-up"></i></button>
                <button class="dislike-btn text-red-500 hover:text-red-700" data-id="${data.response_id}"><i class="fas fa-thumbs-down"></i></button>
            `;
            contentDiv.appendChild(ratingDiv);
        }
        div.appendChild(contentDiv);
    }
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function isValidURL(str) {
    try {
        new URL(str);
        return true;
    } catch {
        return false;
    }
}

function debounce(fn, ms) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn(...args), ms);
    };
}

function updateHistory(page = 1, perPage = 20) {
    const contentDiv = historyBox.querySelector('.history-content') || document.createElement('div');
    contentDiv.className = 'history-content';
    contentDiv.innerHTML = '';
    const start = (page - 1) * perPage;
    const end = start + perPage;
    const paginatedConversations = conversations.slice(start, end);
    paginatedConversations.forEach(conv => {
        const userDiv = document.createElement('div');
        userDiv.className = 'chat-bubble-user';
        userDiv.textContent = escapeHTML(conv.question);
        contentDiv.appendChild(userDiv);

        const botDiv = document.createElement('div');
        botDiv.className = 'chat-bubble-bot';
        botDiv.innerHTML = `
            <strong>Chatbot :</strong> ${escapeHTML(conv.answer)}
            ${conv.link && isValidURL(conv.link) ? `<br><a href="${escapeHTML(conv.link)}" class="text-blue-500 underline" target="_blank">${translations[uiLang.value].link || 'Lien'}</a>` : ''}
            <br><strong>Catégorie :</strong> ${escapeHTML(conv.category)}
            <br><strong>Évaluation :</strong> ${escapeHTML(conv.rating)}
        `;
        contentDiv.appendChild(botDiv);
    });
    if (!historyBox.querySelector('.history-content')) {
        historyBox.appendChild(contentDiv);
    }
    const pagination = document.createElement('div');
    pagination.className = 'flex justify-center mt-4';
    pagination.innerHTML = `
        <button class="px-4 py-2 bg-indigo-600 text-white rounded-lg disabled:opacity-50" 
                ${page === 1 ? 'disabled' : ''} 
                onclick="updateHistory(${page - 1}, ${perPage})">${translations[uiLang.value].previous || 'Précédent'}</button>
        <button class="px-4 py-2 bg-indigo-600 text-white rounded-lg ml-2" 
                ${end >= conversations.length ? 'disabled' : ''} 
                onclick="updateHistory(${page + 1}, ${perPage})">${translations[uiLang.value].next || 'Suivant'}</button>
    `;
    contentDiv.appendChild(pagination);
    historyBox.scrollTop = historyBox.scrollHeight;
}

function updateInterfaceLang(lang) {
    const t = translations[lang];
    document.body.dir = lang === 'ar' ? 'rtl' : 'ltr';
    const elements = {
        title: document.getElementById('title'),
        historyLabel: document.getElementById('historyLabel'),
        clearHistoryLabel: document.getElementById('clearHistoryLabel'),
        pdfLabel: document.getElementById('pdfLabel'),
        imageLabel: document.getElementById('imageLabel'),
        outputLangLabel: document.getElementById('outputLangLabel'),
        voiceLabel: document.getElementById('voiceLabel'),
        exportLabel: document.getElementById('exportLabel'),
        responsePrompt: document.getElementById('responsePrompt'),
        userInput: document.getElementById('userInput'),
        newResponse: document.getElementById('newResponse'),
        newLink: document.getElementById('newLink'),
        submitResponse: document.getElementById('submitResponse')
    };
    if (elements.title) elements.title.textContent = t.title;
    if (elements.historyLabel) elements.historyLabel.textContent = t.historyLabel;
    if (elements.clearHistoryLabel) elements.clearHistoryLabel.textContent = t.clearHistoryLabel;
    if (elements.pdfLabel) elements.pdfLabel.textContent = t.pdfLabel;
    if (elements.imageLabel) elements.imageLabel.textContent = t.imageLabel;
    if (elements.outputLangLabel) elements.outputLangLabel.textContent = t.outputLangLabel;
    if (elements.voiceLabel) elements.voiceLabel.textContent = t.voiceLabel;
    if (elements.exportLabel) elements.exportLabel.textContent = t.exportLabel;
    if (elements.responsePrompt) elements.responsePrompt.textContent = t.responsePrompt;
    if (elements.userInput) elements.userInput.placeholder = t.placeholder;
    if (elements.newResponse) elements.newResponse.placeholder = t.newResponse;
    if (elements.newLink) elements.newLink.placeholder = t.newLink;
    if (elements.submitResponse) elements.submitResponse.textContent = t.submit;
    updateHistory();
}

// Speech Recognition
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }
        userInput.value = finalTranscript + interimTranscript;
        userInput.focus();
        userInput.selectionStart = userInput.selectionEnd = userInput.value.length;
        toggleCancelButton();
    };

    recognition.onerror = (event) => {
        addMessage(`${translations[uiLang.value].error}: ${translations[uiLang.value].speechError} (${event.error})`, false);
        stopRecognition();
    };

    recognition.onend = () => {
        if (isRecognizing) {
            try {
                recognition.start();
            } catch (error) {
                addMessage(`${translations[uiLang.value].error}: ${error.message}`, false);
                stopRecognition();
            }
        } else {
            recordButton.classList.remove('recording', 'bg-red-500', 'animate-pulse');
            recordButton.classList.add('bg-green-500', 'hover:bg-green-600');
            micStatus.classList.add('hidden');
        }
    };
}

function toggleRecording() {
    if (!isRecognizing) {
        startRecognition();
    } else {
        stopRecognition();
    }
}

function startRecognition() {
    if (!recognition) return;
    recognition.lang = uiLang.value === 'ar' ? 'ar-SA' : uiLang.value === 'en' ? 'en-US' : 'fr-FR';
    try {
        userInput.value = '';
        recognition.start();
        isRecognizing = true;
        recordButton.classList.add('bg-red-500', 'hover:bg-red-600', 'animate-pulse');
        recordButton.classList.remove('bg-green-500');
        micStatus.classList.remove('hidden');
        micStatus.textContent = translations[uiLang.value].recording;
    } catch (error) {
        addMessage(`${translations[uiLang.value].error} : ${error.message}`, false);
    }
}

function stopRecognition() {
    if (!recognition) return;
    recognition.stop();
    isRecognizing = false;
    recordButton.classList.remove('bg-red-500', 'hover:bg-red-600', 'animate-pulse');
    recordButton.classList.add('bg-green-500');
    micStatus.classList.add('hidden');
}

// Gestionnaire d'événement pour le bouton d'enregistrement
recordButton.addEventListener('click', toggleRecording);

// Gestionnaire pour le bouton d'annulation
document.getElementById('cancelInput').addEventListener('click', () => {
    userInput.value = '';
    toggleCancelButton();
});

function toggleCancelButton() {
    document.getElementById('cancelInput').classList.toggle('hidden', !userInput.value);
}

userInput.addEventListener('input', toggleCancelButton);

submitResponse.addEventListener('click', async () => {
    const question = responseForm.dataset.question;
    const response = newResponse.value.trim();
    const link = newLink.value.trim();
    const category = newCategory.value;
    if (!response) {
        addMessage(`${translations[uiLang.value].error || 'Erreur'} : ${translations[uiLang.value].noResponse || 'Veuillez entrer une réponse.'}`, false);
        return;
    }

    try {
        const res = await fetch('/add_response', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json', 
                'X-CSRFToken': document.getElementById('csrf_token').value 
            },
            body: JSON.stringify({ question, response, link, category })
        });
        if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorMessages[errorData.error]?.[uiLang.value] || errorData.error || 'Erreur lors de l’ajout de la réponse');
        }
        const data = await res.json();
        if (data.error) throw new Error(errorMessages[data.error]?.[uiLang.value] || data.error);

        responseForm.classList.add('hidden');
        newResponse.value = '';
        newLink.value = '';
        newCategory.value = 'Général';
        addMessage(translations[uiLang.value].responseAdded || "Merci ! Votre réponse a été ajoutée.", false);
        conversations.push({ question, answer: response, link, category, rating: 'Non évalué' });
        if (conversations.length > 100) conversations = conversations.slice(-100);
        localStorage.setItem('conversations', JSON.stringify(conversations));
        updateHistory();
    } catch (error) {
        addMessage(`${translations[uiLang.value].error || 'Erreur'} : ${error.message}`, false);
        console.error('Erreur add_response:', error);
    }
});

chatbox.addEventListener('click', async (e) => {
    if (e.target.classList.contains('like-btn') || e.target.classList.contains('dislike-btn')) {
        const responseId = e.target.dataset.id;
        const rating = e.target.classList.contains('like-btn') ? 'like' : 'dislike';
        try {
            const res = await fetch('/rate', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json', 
                    'X-CSRFToken': document.getElementById('csrf_token').value 
                },
                body: JSON.stringify({ response_id: responseId, rating })
            });
            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorMessages[errorData.error]?.[uiLang.value] || errorData.error || 'Erreur lors de l’enregistrement de l’évaluation');
            }
            const data = await res.json();
            if (data.error) throw new Error(errorMessages[data.error]?.[uiLang.value] || data.error);

            const otherBtn = e.target.classList.contains('like-btn')
                ? e.target.parentElement.querySelector('.dislike-btn')
                : e.target.parentElement.querySelector('.like-btn');
            e.target.classList.add('text-yellow-500', 'font-bold');
            otherBtn.classList.remove('text-yellow-500', 'font-bold');
            e.target.disabled = true;
            otherBtn.disabled = true;
            const index = conversations.findIndex(c => c.response_id === responseId);
            if (index !== -1) {
                conversations[index].rating = rating;
                localStorage.setItem('conversations', JSON.stringify(conversations));
                updateHistory();
            }
        } catch (error) {
            addMessage(`${translations[uiLang.value].error || 'Erreur'} : ${error.message}`, false);
            console.error('Erreur rate:', error);
        }
    }
});

historyButton.addEventListener('click', () => {
    historyBox.classList.toggle('hidden');
    chatbox.classList.toggle('hidden');
    if (!historyBox.classList.contains('hidden')) {
        updateHistory();
    }
});

exportButton.addEventListener('click', async () => {
    if (!conversations || conversations.length === 0) {
        addMessage(`${translations[uiLang.value].error || 'Erreur'} : ${translations[uiLang.value].noConversations || 'Aucune conversation à exporter.'}`, false);
        return;
    }

    exportButton.disabled = true;
    exportButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + (translations[uiLang.value].exporting || 'Exportation...');
    try {
        const response = await fetch('/export_conversations', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json', 
                'X-CSRFToken': document.getElementById('csrf_token').value 
            },
            body: JSON.stringify({ conversations })
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorMessages[errorData.error]?.[uiLang.value] || errorData.error || 'Erreur lors de l’exportation du PDF');
        }
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'conversation.pdf';
        a.click();
        window.URL.revokeObjectURL(url);
        addMessage(translations[uiLang.value].exportSuccess || "PDF exporté avec succès.", false);
    } catch (error) {
        addMessage(`${translations[uiLang.value].error || 'Erreur'} : ${error.message}`, false);
        console.error('Erreur export PDF:', error);
    } finally {
        exportButton.disabled = false;
        exportButton.innerHTML = '<i class="fas fa-file-pdf mr-2"></i> <span id="exportLabel">' + (translations[uiLang.value].exportLabel || 'Exporter') + '</span>';
    }
});

userInput.addEventListener('keypress', debounce((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendButton.click();
    }
}, 200));

document.getElementById('clearHistoryButton').addEventListener('click', () => {
    conversations = [];
    localStorage.setItem('conversations', JSON.stringify(conversations));
    historyBox.querySelector('.history-content').innerHTML = `<p class="text-gray-500">${translations[uiLang.value].historyCleared || 'Historique vidé.'}</p>`;
});

updateInterfaceLang(uiLang.value);
</script>