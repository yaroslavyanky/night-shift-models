from pathlib import Path
import json,struct,io
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[1];results=[]
for path in sorted((root/'Assets/NightShift/GLB').glob('*.glb')):
    data=path.read_bytes();magic,ver,total=struct.unpack_from('<III',data)
    assert magic==0x46546C67 and ver==2 and total==len(data)
    jlen,jtype=struct.unpack_from('<II',data,12);assert jtype==0x4E4F534A
    doc=json.loads(data[20:20+jlen]);bpos=20+jlen
    blen,btype=struct.unpack_from('<II',data,bpos);assert btype==0x004E4942 and bpos+8+blen==len(data)
    binary=data[bpos+8:];assert doc['buffers'][0]['byteLength']==len(binary)
    for v in doc['bufferViews']:assert v.get('byteOffset',0)%4==0 and v.get('byteOffset',0)+v['byteLength']<=len(binary)
    def acc(i):
        a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']];assert a['componentType']==5126
        width={'VEC2':2,'VEC3':3}[a['type']];size=a['count']*width*4;assert size<=v['byteLength']
        p=np.frombuffer(binary,dtype='<f4',count=a['count']*width,offset=v['byteOffset']).reshape(-1,width)
        assert np.isfinite(p).all()
        if 'min' in a:assert np.allclose(p.min(0),a['min']) and np.allclose(p.max(0),a['max'])
        return p
    triangles=0
    for prim in doc['meshes'][0]['primitives']:
        p=acc(prim['attributes']['POSITION']);n=acc(prim['attributes']['NORMAL']);uv=acc(prim['attributes']['TEXCOORD_0'])
        assert len(p)==len(n)==len(uv) and len(p)%3==0
        assert np.allclose(np.linalg.norm(n,axis=1),1,atol=1e-5)
        t=p.reshape(-1,3,3);cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);assert (np.linalg.norm(cross,axis=1)>1e-10).all()
        assert (np.sum(cross*n[::3],axis=1)>0).all(), (path.name, np.where(np.sum(cross*n[::3],axis=1)<=0)[0].tolist())
        triangles+=len(p)//3
    for image in doc['images']:
        v=doc['bufferViews'][image['bufferView']];png=binary[v['byteOffset']:v['byteOffset']+v['byteLength']]
        im=Image.open(io.BytesIO(png));assert im.size==(512,512);im.verify()
    results.append({'model':path.stem,'triangles':triangles,'status':'valid'})
# OBJ exports should carry the same triangle count as GLB.
for r in results:
    obj=root/'Assets/NightShift/Models'/f'{r["model"]}.obj'
    assert sum(l.startswith('f ') for l in obj.read_text().splitlines())==r['triangles']
report={'models':len(results),'triangles':sum(r['triangles'] for r in results),'format':'glTF 2.0 binary + OBJ','checks':['GLB chunk and buffer layout','accessor counts and bounds','finite values','unit normals','triangle winding and nonzero area','embedded PNG integrity','OBJ/GLB triangle parity'],'godot_editor_validation':'not run; Godot is not installed','results':results}
(root/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['models','triangles','godot_editor_validation']}))
