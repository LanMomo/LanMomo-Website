module.exports = {
  server: {
    hostname: 'localhost',
    port: 3000
  },
  url: {
    root: 'http://localhost:3000'
  },
  mailer: {
    from: {
      name: 'LAN Montmorency',
      address: 'user@gmail.com'
    },
    transportOptions: {
      host: 'smtp.gmail.com',
      port: 465,
      secure: true,
      authMethod: 'LOGIN',
      auth: {
        user: 'user@gmail.com',
        pass: 'password'
      }
    }
  },
  db: {
    url: 'mongodb://localhost/dev'
  },
  types: ['pc', 'console'],
  maximum: {
    pc: 50,
    console: 15
  },
  token: 'token',
  games: [
    {
      title: 'Team Fortress 2',
      description: 'FPS multijoueur développé par Valve. Les modes de jeux PVP et Mann Versus Machine seront offert.',
      imagePath: 'assets/game_banners/tf2.jpg'
    },
    {
      title: 'Counter Strike: Source',
      description: 'FPS en équipe développé par Valve. Les modes poser la bombe et délivrer les otages seront offert.',
      imagePath: 'assets/game_banners/css.jpg'
    },
    {
      title: 'CS: Global Offensive',
      description: 'FPS en équipe développé par Valve. Les modes poser la bombe et délivrer les otages seront offert.',
      imagePath: 'assets/game_banners/cs:go.jpg'
    },
    {
      title: 'Minecraft',
      description: 'Sandbox multijoueur développé par Mojang. Une course au dragon coopérative en mode survie sera organisée.',
      imagePath: 'assets/game_banners/minecraft.jpg'
    },
    {
      title: 'Garry\'s Mod',
      description: 'Sandbox multijoueur développé par Facepunch Studios. Les modes Trouble in Terrorist Town et Prop Hunt sont prévus.',
      imagePath: 'assets/game_banners/gmod.jpg'
    },
    {
      title: 'TrackMania Nations Forever',
      description: 'Jeux de course multijoueur développé par Nadeo.',
      imagePath: 'assets/game_banners/tmnations.jpg'
    },
    {
      title: 'Unreal Tournament 2004',
      description: 'FPS futuriste développé par Epic Games et Digital Extremes.',
      imagePath: 'assets/game_banners/ut2004.jpg'
    },
    {
      title: 'League of Legends',
      description: 'Arène de bataille multijoueur développée par Riot Games.',
      imagePath: 'assets/game_banners/lol.jpg'
    }
  ]
};
