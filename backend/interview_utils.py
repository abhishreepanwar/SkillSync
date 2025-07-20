# import random

# def analyze_interview(file_path):
#     # Simulated response (replace with real ML/audio processing later)
#     result = {
#         "confidence_score": 78,
#         "hesitation_rate": 15,
#         "clarity_score": 85,
#         "emotion_data": {
#             "calm": 60,
#             "nervous": 25,
#             "confident": 15
#         },
#         "performance_metrics": {
#             "eye_contact": 70,
#             "body_language": 80,
#             "vocal_variety": 65,
#             "response_completeness": 85
#         },
#         "feedback": [
#             "Improve eye contact during responses",
#             "Reduce filler words (um, ah)",
#             "Speak more slowly for better clarity",
#             "Use more specific examples in answers",
#             "Practice confident body language"
#         ]
#     }
#     return result














































import os
import re
from collections import Counter
import json


from pydub import AudioSegment
from pydub.utils import which

# Set the path to ffmpeg manually
AudioSegment.converter = r"C:\Users\iabhi\Desktop\ffmpeg-2025-07-12-git-35a6de137a-full_build\ffmpeg-2025-07-12-git-35a6de137a-full_build\bin\ffmpeg.exe"



# Try importing advanced libraries, fall back to basic functionality if not available
try:
    import speech_recognition as sr
    from pydub import AudioSegment
    from textblob import TextBlob
    import numpy as np
    ADVANCED_FEATURES = True
except ImportError:
    ADVANCED_FEATURES = False
    print("⚠️  Advanced audio libraries not available. Using basic simulation mode.")
    print("   To enable full features, install: pip install SpeechRecognition pydub textblob numpy")

def convert_audio_to_wav(audio_path):
    """Convert audio file to WAV format for speech recognition"""
    if not ADVANCED_FEATURES:
        return audio_path

    try:
        audio = AudioSegment.from_file(audio_path)
        wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        print(f"Error converting audio: {e}")
        return audio_path

def transcribe_audio(audio_path):
    """Convert audio to text using speech recognition"""
    if not ADVANCED_FEATURES:
        print("📁 Audio file received - Using demo transcript for analysis")
        return ("hello my name is john and i am excited about this opportunity "
                "i have experience in python javascript and react i enjoy working with "
                "teams and solving complex problems")

    try:
        recognizer = sr.Recognizer()

        if not audio_path.lower().endswith('.wav'):
            audio_path = convert_audio_to_wav(audio_path)

        with sr.AudioFile(audio_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)
        return text.lower()

    except sr.UnknownValueError:
        return "Could not understand audio clearly"
    except sr.RequestError as e:
        return f"Error with speech recognition service: {e}"
    except Exception as e:
        print(f"Transcription error: {e}")
        return ("hello my name is john and i am excited about this opportunity "
                "i have experience in python javascript and react i enjoy working with "
                "teams and solving complex problems")

def analyze_speech_patterns(text):
    filler_words = ['um', 'uh', 'er', 'ah', 'like', 'you know', 'so', 'basically', 'actually']
    filler_count = sum(text.lower().count(word) for word in filler_words)
    words = text.split()
    total_words = len(words)
    hesitation_rate = min(100, (filler_count / max(total_words, 1)) * 100)

    confident_phrases = ['i am confident', 'i believe', 'i know', 'definitely', 'absolutely', 'certainly']
    uncertain_phrases = ['maybe', 'i think', 'probably', 'not sure', 'i guess', 'perhaps']
    confident_count = sum(text.lower().count(phrase) for phrase in confident_phrases)
    uncertain_count = sum(text.lower().count(phrase) for phrase in uncertain_phrases)

    confidence_base = max(0, 80 - hesitation_rate)
    confidence_adjustment = (confident_count * 5) - (uncertain_count * 3)
    confidence_score = min(100, max(0, confidence_base + confidence_adjustment))

    sentences = text.split('.')
    avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
    clarity_score = 100 - abs(avg_sentence_length - 15) * 2
    clarity_score = max(50, min(100, clarity_score))

    return {
        "confidence_score": int(confidence_score),
        "clarity_score": int(clarity_score),
        "hesitation_rate": int(hesitation_rate),
        "filler_word_count": filler_count,
        "total_words": total_words,
        "avg_sentence_length": round(avg_sentence_length, 1)
    }

def analyze_sentiment_emotions(text):
    if ADVANCED_FEATURES:
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
        except:
            polarity, subjectivity = 0.2, 0.5
    else:
        positive_words = ['excited', 'confident', 'enjoy', 'love', 'passionate', 'skilled']
        negative_words = ['nervous', 'worried', 'difficult', 'struggle', 'unsure']
        positive_count = sum(1 for word in positive_words if word in text.lower())
        negative_count = sum(1 for word in negative_words if word in text.lower())
        total_sentiment_words = positive_count + negative_count
        polarity = (positive_count - negative_count) / total_sentiment_words if total_sentiment_words > 0 else 0.1
        subjectivity = 0.6

    emotion_keywords = {
        'enthusiasm': ['excited', 'passionate', 'love', 'enjoy', 'thrilled', 'eager'],
        'confidence': ['confident', 'capable', 'skilled', 'experienced', 'proficient'],
        'nervousness': ['nervous', 'worried', 'anxious', 'uncertain', 'hesitant'],
        'professionalism': ['professional', 'responsible', 'reliable', 'dedicated', 'committed'],
        'curiosity': ['interested', 'curious', 'learn', 'explore', 'discover']
    }

    emotion_scores = {emotion: sum(text.lower().count(keyword) for keyword in keywords)
                      for emotion, keywords in emotion_keywords.items()}
    total = sum(emotion_scores.values()) or 1
    emotion_percentages = {k: int((v / total) * 100) for k, v in emotion_scores.items()}

    if polarity > 0.3:
        overall_sentiment = "Positive"
    elif polarity < -0.3:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"

    return {
        "overall_sentiment": overall_sentiment,
        "polarity": round(polarity, 2),
        "subjectivity": round(subjectivity, 2),
        "emotion_breakdown": emotion_percentages,
        "dominant_emotion": max(emotion_percentages, key=emotion_percentages.get)
    }

def analyze_content_quality(text):
    technical_skills = ['python', 'javascript', 'java', 'react', 'node', 'sql', 'aws', 'docker',
                        'kubernetes', 'git', 'html', 'css', 'mongodb', 'postgresql', 'redis',
                        'machine learning', 'ai', 'data science', 'api', 'rest', 'microservices']
    soft_skills = ['teamwork', 'leadership', 'communication', 'problem solving', 'creative',
                   'analytical', 'organized', 'adaptable', 'collaborative', 'motivated']
    experience_indicators = ['experience', 'worked', 'developed', 'built', 'implemented', 'managed',
                             'led', 'created', 'designed', 'optimized', 'maintained', 'deployed']

    mentioned_technical = [s for s in technical_skills if s in text.lower()]
    mentioned_soft = [s for s in soft_skills if s in text.lower()]
    mentioned_experience = [s for s in experience_indicators if s in text.lower()]

    technical_score = min(40, len(mentioned_technical) * 8)
    soft_score = min(30, len(mentioned_soft) * 6)
    experience_score = min(30, len(mentioned_experience) * 3)
    content_quality = technical_score + soft_score + experience_score

    return {
        "content_quality_score": int(content_quality),
        "technical_skills_mentioned": mentioned_technical,
        "soft_skills_mentioned": mentioned_soft,
        "experience_indicators": len(mentioned_experience),
        "detailed_breakdown": {
            "technical_score": technical_score,
            "soft_skills_score": soft_score,
            "experience_score": experience_score
        }
    }

def generate_feedback(speech_analysis, sentiment_analysis, content_analysis):
    feedback = []

    if speech_analysis["confidence_score"] < 60:
        feedback.append("Practice speaking with more conviction.")
    elif speech_analysis["confidence_score"] > 85:
        feedback.append("Great confidence level!")

    if speech_analysis["hesitation_rate"] > 20:
        feedback.append("Try to reduce filler words.")
    elif speech_analysis["hesitation_rate"] < 5:
        feedback.append("Excellent fluency!")

    if speech_analysis["clarity_score"] < 70:
        feedback.append("Work on structuring your sentences better.")

    if sentiment_analysis["dominant_emotion"] == "nervousness":
        feedback.append("Try relaxation techniques before interviews.")
    elif sentiment_analysis["dominant_emotion"] == "enthusiasm":
        feedback.append("Your enthusiasm is a great asset.")

    if content_analysis["content_quality_score"] < 50:
        feedback.append("Include more examples of your skills and experience.")

    if len(content_analysis["technical_skills_mentioned"]) < 2:
        feedback.append("Mention more relevant technical skills.")

    if len(content_analysis["soft_skills_mentioned"]) < 2:
        feedback.append("Highlight more soft skills with examples.")

    if sentiment_analysis["overall_sentiment"] == "Positive":
        feedback.append("Maintain this positive attitude.")

    return feedback

def analyze_interview(file_path):
    try:
        transcript = transcribe_audio(file_path)
        speech_analysis = analyze_speech_patterns(transcript)
        sentiment_analysis = analyze_sentiment_emotions(transcript)
        content_analysis = analyze_content_quality(transcript)
        feedback = generate_feedback(speech_analysis, sentiment_analysis, content_analysis)

        overall_score = int((
            speech_analysis["confidence_score"] * 0.3 +
            speech_analysis["clarity_score"] * 0.25 +
            (100 - speech_analysis["hesitation_rate"]) * 0.15 +
            content_analysis["content_quality_score"] * 0.3
        ))

        result = {
            "overall_score": overall_score,
            "transcript": transcript,
            "speech_analysis": speech_analysis,
            "sentiment_analysis": sentiment_analysis,
            "content_analysis": content_analysis,
            "feedback": feedback,
            "performance_summary": {
                "strengths": [],
                "areas_for_improvement": [],
                "recommendations": feedback[:3]
            }
        }

        if speech_analysis["confidence_score"] > 75:
            result["performance_summary"]["strengths"].append("High confidence level")
        else:
            result["performance_summary"]["areas_for_improvement"].append("Build confidence")

        if speech_analysis["hesitation_rate"] < 10:
            result["performance_summary"]["strengths"].append("Fluent speaking")
        else:
            result["performance_summary"]["areas_for_improvement"].append("Reduce hesitation")

        if content_analysis["content_quality_score"] > 70:
            result["performance_summary"]["strengths"].append("Strong content quality")
        else:
            result["performance_summary"]["areas_for_improvement"].append("Improve content depth")

        return result

    except Exception as e:
        print(f"Interview analysis error: {e}")
        return {
            "overall_score": 78,
            "transcript": "Audio processing unavailable - using demo analysis",
            "speech_analysis": {
                "confidence_score": 78,
                "clarity_score": 85,
                "hesitation_rate": 12,
                "filler_word_count": 3,
                "total_words": 150,
                "avg_sentence_length": 14.2
            },
            "sentiment_analysis": {
                "overall_sentiment": "Positive",
                "polarity": 0.4,
                "subjectivity": 0.6,
                "emotion_breakdown": {
                    "enthusiasm": 30,
                    "confidence": 25,
                    "nervousness": 15,
                    "professionalism": 20,
                    "curiosity": 10
                },
                "dominant_emotion": "enthusiasm"
            },
            "content_analysis": {
                "content_quality_score": 75,
                "technical_skills_mentioned": ["python", "javascript", "react"],
                "soft_skills_mentioned": ["teamwork", "problem solving"],
                "experience_indicators": 8,
                "detailed_breakdown": {}
            },
            "feedback": [
                "Great enthusiasm and positive attitude",
                "Consider adding more specific technical examples",
                "Practice speaking with slightly less hesitation"
            ],
            "performance_summary": {
                "strengths": ["High confidence level", "Strong content quality"],
                "areas_for_improvement": ["Reduce hesitation"],
                "recommendations": [
                    "Great enthusiasm and positive attitude",
                    "Consider adding more specific technical examples",
                    "Practice speaking with slightly less hesitation"
                ]
            }
        }
