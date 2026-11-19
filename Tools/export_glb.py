"""glTF 2.0 binary export with embedded PNG textures, metres, authored pivots."""
import struct
outdir=ASSETS/'GLB';outdir.mkdir(exist_ok=True)
for mesh in models:
    binary=bytearray();views=[];accessors=[]
    def view(data,target=None):
        while len(binary)%4:binary.append(0)
        start=len(binary);binary.extend(data);v={'buffer':0,'byteOffset':start,'byteLength':len(data)}
        if target:v['target']=target
        views.append(v);return len(views)-1
    def accessor(a,kind):
        a=np.asarray(a,dtype='<f4');v=view(a.tobytes(),34962)
        acc={'bufferView':v,'componentType':5126,'count':len(a),'type':kind}
        if kind=='VEC3':acc.update(min=a.min(0).tolist(),max=a.max(0).tolist())
        accessors.append(acc);return len(accessors)-1
    used=list(dict.fromkeys(mat for _,mat,_ in mesh.faces));mats=[];images=[];textures=[];prims=[]
    for mat in used:
        imageview=view((ASSETS/'Textures'/f'{mat}.png').read_bytes())
        images.append({'bufferView':imageview,'mimeType':'image/png','name':mat})
        textures.append({'sampler':0,'source':len(images)-1})
        material={'name':mat,'pbrMetallicRoughness':{'baseColorTexture':{'index':len(textures)-1},'metallicFactor':.4 if mat=='steel' else 0,'roughnessFactor':.85},'doubleSided':False}
        mats.append(material);positions=[];normals=[];uvs=[]
        for p,mt,uv in mesh.faces:
            if mt!=mat:continue
            normal=np.cross(p[1]-p[0],p[2]-p[0]);normal/=np.linalg.norm(normal)
            for k in range(1,len(p)-1):
                for i in [0,k,k+1]:positions.append(p[i]);normals.append(normal);uvs.append((uv[i][0],1-uv[i][1]))
        prims.append({'attributes':{'POSITION':accessor(positions,'VEC3'),'NORMAL':accessor(normals,'VEC3'),'TEXCOORD_0':accessor(uvs,'VEC2')},'material':len(mats)-1,'mode':4})
    while len(binary)%4:binary.append(0)
    doc={'asset':{'version':'2.0','generator':'NightShift procedural asset tools'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'name':mesh.name,'mesh':0}],'meshes':[{'name':mesh.name,'primitives':prims}],'materials':mats,'images':images,'textures':textures,'samplers':[{'magFilter':9729,'minFilter':9987,'wrapS':10497,'wrapT':10497}],'buffers':[{'byteLength':len(binary)}],'bufferViews':views,'accessors':accessors}
    js=json.dumps(doc,separators=(',',':')).encode();js+=b' '*((-len(js))%4)
    payload=struct.pack('<II',len(js),0x4E4F534A)+js+struct.pack('<II',len(binary),0x004E4942)+binary
    (outdir/f'{mesh.name}.glb').write_bytes(struct.pack('<III',0x46546C67,2,12+len(payload))+payload)
print('Exported',len(models),'self-contained GLB models')
