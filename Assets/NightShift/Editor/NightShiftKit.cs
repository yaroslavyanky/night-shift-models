#if UNITY_EDITOR
using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.SceneManagement;

// Run explicitly from Tools; importing the kit never changes the open scene.
public static class NightShiftKit
{
    const string Root = "Assets/NightShift";
    static readonly string[] Names = { "Floor_3m", "Wall_3m", "DoorFrame", "Door_17", "Locker", "FuseBox", "Bench", "Pipe", "WallLamp", "Flashlight", "Fuse", "Crate" };

    [MenuItem("Tools/Night Shift/Build prefabs and demo scene")]
    public static void Build()
    {
        string[] missing = Names.Where(n => AssetDatabase.LoadAssetAtPath<GameObject>($"{Root}/Models/{n}.obj") == null).ToArray();
        if (missing.Length > 0)
            throw new InvalidOperationException("Missing models. Copy the complete Assets/NightShift folder and wait for import: " + string.Join(", ", missing));
        Directory.CreateDirectory($"{Root}/Materials");
        Directory.CreateDirectory($"{Root}/Prefabs");
        Directory.CreateDirectory($"{Root}/Scenes");
        AssetDatabase.Refresh();
        var shader = Shader.Find(GraphicsSettings.currentRenderPipeline == null ? "Standard" : "Universal Render Pipeline/Lit");
        if (shader == null) throw new InvalidOperationException("Use a Universal 3D (URP) project or the Standard render pipeline.");
        var materials = new Dictionary<string, Material>();
        foreach (var path in Directory.GetFiles($"{Root}/Textures", "*.png"))
        {
            string name = Path.GetFileNameWithoutExtension(path);
            string assetPath = path.Replace('\\', '/');
            var texture = AssetDatabase.LoadAssetAtPath<Texture2D>(assetPath);
            var materialPath = $"{Root}/Materials/{name}.mat";
            var material = AssetDatabase.LoadAssetAtPath<Material>(materialPath);
            if (material == null) { material = new Material(shader); AssetDatabase.CreateAsset(material, materialPath); }
            material.shader = shader;
            material.mainTexture = texture;
            material.color = Color.white;
            if (material.HasProperty("_Smoothness")) material.SetFloat("_Smoothness", .12f);
            if (material.HasProperty("_Glossiness")) material.SetFloat("_Glossiness", .12f);
            if (material.HasProperty("_Metallic")) material.SetFloat("_Metallic", name == "steel" ? .55f : 0f);
            EditorUtility.SetDirty(material);
            materials[name] = material;
        }
        foreach (var name in Names)
        {
            var source = AssetDatabase.LoadAssetAtPath<GameObject>($"{Root}/Models/{name}.obj");
            var instance = UnityEngine.Object.Instantiate(source);
            instance.name = name;
            try
            {
                foreach (var renderer in instance.GetComponentsInChildren<MeshRenderer>())
                {
                    var assigned = renderer.sharedMaterials;
                    for (int i = 0; i < assigned.Length; i++)
                    {
                        string key = assigned[i] == null ? "" : assigned[i].name.Replace(" (Instance)", "").Trim();
                        if (!materials.TryGetValue(key, out var material))
                            throw new InvalidOperationException($"Unknown material '{key}' on {name}. Keep NightShift.mtl beside the OBJ files.");
                        assigned[i] = material;
                    }
                    renderer.sharedMaterials = assigned;
                    var filter = renderer.GetComponent<MeshFilter>();
                    if (filter != null && filter.sharedMesh != null)
                        renderer.gameObject.AddComponent<MeshCollider>().sharedMesh = filter.sharedMesh;
                }
                PrefabUtility.SaveAsPrefabAsset(instance, $"{Root}/Prefabs/{name}.prefab");
            }
            finally { UnityEngine.Object.DestroyImmediate(instance); }
        }
        AssetDatabase.SaveAssets();
        var previous = SceneManager.GetActiveScene();
        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
        SceneManager.SetActiveScene(scene);
        try
        {
            Place("Floor_3m", Vector3.zero);
            Place("Wall_3m", new Vector3(0,0,-1.5f));
            Place("Wall_3m", new Vector3(-1.5f,0,0),90);
            Place("Locker", new Vector3(-.9f,0,-1.18f));
            Place("FuseBox", new Vector3(.75f,1.15f,-1.29f));
            Place("Bench", new Vector3(-.9f,0,.2f),90);
            Place("Pipe", new Vector3(1.3f,0,-1.25f));
            Place("WallLamp", new Vector3(.5f,2.5f,-1.35f));
            Place("Crate", new Vector3(.9f,0,.7f));
            Place("Flashlight", new Vector3(.9f,.55f,.7f));
            Place("Fuse", new Vector3(.7f,.55f,.7f));
            // A separate doorway bay, with the door pivot retained at the hinge.
            Place("Floor_3m", new Vector3(3,0,0));
            Place("DoorFrame", new Vector3(3,0,-1.4f));
            var door = Place("Door_17", new Vector3(3,.04f,-1.4f));
            var bounds = door.GetComponentsInChildren<Renderer>().First().bounds;
            foreach (var renderer in door.GetComponentsInChildren<Renderer>()) bounds.Encapsulate(renderer.bounds);
            door.transform.position += Vector3.right * (3 - bounds.center.x);
            var camera = new GameObject("Preview camera", typeof(Camera)).GetComponent<Camera>();
            camera.tag = "MainCamera";
            camera.transform.position = new Vector3(6,4.5f,7);
            camera.transform.LookAt(new Vector3(1,1,0));
            camera.orthographic = true; camera.orthographicSize = 3.1f;
            camera.clearFlags = CameraClearFlags.SolidColor; camera.backgroundColor = new Color(.06f,.08f,.075f);
            camera.nearClipPlane = .02f; camera.farClipPlane = 100;
            var key = new GameObject("Preview key light", typeof(Light)).GetComponent<Light>();
            key.type = LightType.Directional; key.intensity = 1.8f;
            key.transform.rotation = Quaternion.Euler(45,-30,0); key.shadows = LightShadows.Soft;
            RenderSettings.ambientMode = AmbientMode.Flat;
            RenderSettings.ambientLight = new Color(.3f,.33f,.3f);
            string scenePath = AssetDatabase.GenerateUniqueAssetPath($"{Root}/Scenes/ArtPreview.unity");
            EditorSceneManager.SaveScene(scene, scenePath);
            Selection.activeObject = AssetDatabase.LoadAssetAtPath<SceneAsset>(scenePath);
            Debug.Log("Night Shift: 12 prefabs and a demo scene created at " + scenePath);
        }
        finally
        {
            EditorSceneManager.CloseScene(scene, true);
            if (previous.IsValid() && previous.isLoaded) SceneManager.SetActiveScene(previous);
        }
        AssetDatabase.SaveAssets();
    }
    static GameObject Place(string name, Vector3 position, float yaw = 0)
    {
        var prefab = AssetDatabase.LoadAssetAtPath<GameObject>($"{Root}/Prefabs/{name}.prefab");
        var instance = (GameObject)PrefabUtility.InstantiatePrefab(prefab);
        instance.transform.SetPositionAndRotation(position, Quaternion.Euler(0,yaw,0));
        return instance;
    }
}
#endif
